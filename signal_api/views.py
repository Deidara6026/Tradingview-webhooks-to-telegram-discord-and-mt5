from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.conf import settings
import telebot
import requests, datetime
import hashlib
import hmac
import logging



std_logger = logging.getLogger(__name__)
lemon_logger = logging.getLogger("lemon")


def send_telegram_message(data: list):
    telegram_settings = settings.TELEGRAM
    bot = telebot.TeleBot(telegram_settings["token"])
    for x in data:
        try:
            bot.send_message(x[0], x[1])
        except:
            pass


def send_discord_message(data: list):
    discord_settings = settings.DISCORD
    for x in data:
        try:
            webhook_url = x[0]
            message = x[1]
            requests.post(webhook_url, json={"content": message})
        except Exception as e:
            pass


def parse_signal_hit(msg: str):
    params = msg.split()
    command = params[0]
    if command.lower() == "close":
        d = {"side": "close"}
        if len(params) > 1:
            d.update({"symbol": params[1]})
    else:
        d = {"symbol": params[1], "side": command}
        for param in params:
            if ":" in param:
                key, value = param.split(":")
                if key.lower() in ["p", "price"]:
                    d.update({"price": value})
                if key.lower().startswith("tp"):
                    d.setdefault("tp", []).append(value)
                if key.lower() in ["sl"]:
                    d.update({"sl": value})

    print(d)
    return d


def parse(params: dict, webhook):
    default_template = """
{{side}} {{symbol}}

Entry Price: {{p}}

Take Profit: {{tp}}
Stop Loss: {{sl}}

        """
    if webhook.message_format == None:
        template = default_template
    else:
        template = webhook.message_format
    m = template
    if "symbol" in params:
        m = m.replace("{{symbol}}", params.get("symbol", "").upper())
    else:
        m = m.replace("{{symbol}}", "")
    if "price" in params:
        m = m.replace("{{price}}", params.get("price", ""))
        m = m.replace("{{p}}", params.get("price", ""))
    else:
        m = m.replace("Entry Price: {{p}}", "")
    if "tp" in params:
        tp_values = ", ".join(map(str, params.get("tp", [])))
        m = m.replace("{{take profit}}", tp_values)
        m = m.replace("{{tp}}", tp_values)
    else:
        m = m.replace("Take Profit: {{tp}}", "")
    if "sl" in params:
        m = m.replace("{{stop loss}}", params.get("sl", ""))
        m = m.replace("{{sl}}", params.get("sl", ""))
    else:
        m = m.replace("Stop Loss: {{sl}}", "")
    if "side" in params:
        m = m.replace("{{side}}", params.get("side", "").upper())
    else:
        m = m.replace("{{side}}", "").replace("{{symbol}}", "")
    return m


class TelegramAPIView(APIView):
    def post(self, request, *args, **kwargs):
        telegram_webhook = get_object_or_404(Telegram_Webhook, id=self.kwargs["pk"])
        if telegram_webhook.hits > telegram_webhook.limit:
            return JsonResponse({"status": "limit exceeded"})

        data = request.data
        telegram_chats = telegram_webhook.telegramchat_set.all()
        tradingview_message = data.get("message")
        params = parse_signal_hit(tradingview_message)
        if telegram_chats:
            data = parse(params, telegram_webhook)
        res = [[chat.chat_id, data] for chat in telegram_chats]

        send_telegram_message(res)
        telegram_webhook.hits += 1
        telegram_webhook.save()
        return JsonResponse({"status": "success"})


class MT5APIView(APIView):
    def post(self, *args, **kwargs):
        mt5_webhook = get_object_or_404(MT5_Webhook, id=self.kwargs["pk"])
        if mt5_webhook.hits > mt5_webhook.limit:
            return JsonResponse({"status": "limit exceeded"})
        data = request.data
        tradingview_messages = data.get("message").split("\n")
        for message in tradingview_messages:
            params = parse_signal_hit(message)
            if params.get("side").lower() == "close":
                o = Order.objects.create(
                    is_active=True,
                    mt5_webhook=mt5_webhook,
                    ticker=params.get("symbol", ""),
                    side=params.get("side", ""),
                )
                o.mt5_webhook = mt5_webhook
                o.save()
                return
            else:
                o = Order.objects.create(
                    is_active=True,
                    mt5_webhook=mt5_webhook,
                    entry=params.get("entry", 0.0),
                    sl=params.get("sl", 0.0),
                    side=params.get("side", ""),
                    ticker=params.get("symbol", ""),
                    quantity=params.get("quantity", ""),
                )
                o.mt5_webhook = mt5_webhook
                o.save()
                tp_values = params.get("tp", [])
                for tp_value in tp_values:
                    tp = TakeProfit.objects.create(
                        is_active=True, order=o, price=tp_value
                    )
                    tp.save()


class DiscordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        discord_webhook = get_object_or_404(Discord_Webhook, id=self.kwargs["pk"])
        if discord_webhook.hits > discord_webhook.limit:
            return JsonResponse({"status": "limit exceeded"})

        data = request.data
        discord_chats = discord_webhook.discordchat_set.all()
        tradingview_message = data.get("message")
        params = parse_signal_hit(tradingview_message)
        if discord_chats:
            data = parse(params, discord_webhook)
        res = [[chat.channel_webhook_url, data] for chat in discord_chats]
        send_discord_message(res)
        discord_webhook.hits += 1
        discord_webhook.save()
        return JsonResponse({"status": "success"})


def handle_lemon_webhook(id, wid, reason):
    url = f"https://api.lemonsqueezy.com/v1/subscriptions/{str(id)}"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {settings.LEMONSQUEEZY['api_key']}",
    }
    result = requests.get(url, headers=headers).json()
    pid = result["data"]["attributes"]["product_id"]
    vid = result["data"]["attributes"]["variant_id"]
    status = result["data"]["attributes"]["status"]
    renews_at = result["data"]["attributes"]["renews_at"]

    if pid == settings.LEMONSQUEEZY["telegram_pid"]:
        t = Telegram_Webhook.objects.filter(webhook_id=wid).first()


    elif pid == settings.LEMONSQUEEZY["discord_pid"]:
        t = Discord_Webhook.objects.filter(webhook_id=wid).first()


    elif pid == settings.LEMONSQUEEZY["mt5_pid"]:
        t = MT5_Webhook.objects.filter(webhook_id=wid).first()


    if reason == "subscription_created":
        t.variant_id = vid
        t.product_id = pid
        t.subscription_id = id
        t.status = "active"
        t.renews_at = datetime.datetime.strptime(renews_at, "%Y-%m-%dT%H:%M:%S.%fZ")

        if vid in settings.LEMONSQUEEZY["telegram_vids"]:
            hit_limit = settings.LEMONSQUEEZY["telegram_vids"][vid]
            t.hit_limit = hit_limit
            t.chat_limit = int(
                result["data"]["attributes"]["first_subscription_item"]["quantity"]
            )

        if vid in settings.LEMONSQUEEZY["discord_vids"]:
            hit_limit = settings.LEMONSQUEEZY["discord_vids"][vid]
            t.hit_limit = hit_limit
            t.chat_limit = int(
                result["data"]["attributes"]["first_subscription_item"]["quantity"]
            )
        
        if vid in settings.LEMONSQUEEZY["mt5_vids"]:
            hit_limit = settings.LEMONSQUEEZY["mt5_vids"][vid]
            t.hit_limit = hit_limit


    elif status in ["past_due", "unpaid"]:
        ends_at = result["data"]["attributes"]["ends_at"]
        t.ends_at = datetime.datetime.strptime(ends_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    elif status == "active":
        t.ends_at = None
        t.status = "active"

    elif status == "on_trial":
        t.status = "active"
        t.ends_at = datetime.datetime.strptime(
            result["data"]["attributes"]["trial_ends_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )

    elif status == "expired":
        t.status = "inactive"

    t.save()

    return [pid, vid]


class LemonAPIView(APIView):
    def post(self, request, *args, **kwargs):
        signature = request.META['HTTP_X_SIGNATURE']
        secret = settings.lemon_signed_secret

        digest = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(digest, signature):
            pass
            #logging here
        data = request.POST
        subscription_id = data["data"]["attributes"]["subscription_id"]
        reason = data["meta"]["event_name"]
        if reason == "renewal":
            return
        webhook_id = data["meta"]["custom_data"]["webhook_id"]
        handle_lemon_webhook(subscription_id, webhook_id, reason)

        return JsonResponse({"status": "success"})


class EAAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mt5_account = get_object_or_404(MT5_Webhook, webhook_id=self.kwargs["pk"])
        order = Order.objects.filter(is_active=True, mt5_webhook=mt5_account).first()
        if not order:
            return JsonResponse({"status": "no orders"})

        tps = order.takeprofit_set.filter(is_active=True).all()
        if not tps:
            order.is_active = False
            order.save()
            return JsonResponse({"status": "no orders"})

        tp = tps.first()
        tp.is_active = False
        tp.save()
        return JsonResponse(
            {
                "status": "success",
                "command": "neworder",
                "entry": order.entry,
                "sl": order.sl,
                "tp": tp.price,
                "ticker": order.ticker,
                "side": order.side,
            }
        )
