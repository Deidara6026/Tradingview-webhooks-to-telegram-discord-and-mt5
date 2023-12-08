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


def send_telegram_message(data: list):
    telegram_settings = settings.TELEGRAM
    bot = telebot.TeleBot(telegram_settings["token"])
    for x in data:
        try:
            bot.send_message(x[0], x[1])
        except:
            pass


def parse_signal_hit(msg: str):
    note = ""
    if "note:" in msg:
        print("note found")
        note = msg.split("note:")[1]
        msg = msg.split("note:")[0]

    params = msg.split()
    d = {"symbol": params[1], "side": params[0]}
    for param in params:
        if ":" in param:
            if param.split(":")[0].lower() in ["p", "price"]:
                d.update({"price": param.split(":")[1]})
            if param.split(":")[0].lower() in ["tp"]:
                d.update({"tp": param.split(":")[1]})
            if param.split(":")[0].lower() in ["sl"]:
                d.update({"sl": param.split(":")[1]})
    d.update({"note": note})

    print(d)
    return d


def parse(params: dict, webhook, chats):
    res = []
    default_template = """
{{side}} {{symbol}}

Entry Price: {{p}}

Take Profit: {{tp}}
Stop Loss: {{sl}}

Comment: {{note}}
        """

    for chat in chats:
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
            m = m.replace("{{take profit}}", params.get("tp", ""))
            m = m.replace("{{tp}}", params.get("tp", ""))
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
        if "note" in params:
            m = m.replace("{{note}}", params.get("note", ""))
        else:
            m = m.replace("Comment: {{note}}", "")
        res.append([chat.chat_id, m])
    return res


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
            data = parse(params, telegram_webhook, telegram_chats)
        send_telegram_message(data)
        telegram_webhook.hits += 1
        telegram_webhook.save()
        return JsonResponse({"status": "success"})


class MT5APIView(APIView):
    def post(self, *args, **kwargs):
        mt5_webhook = get_object_or_404(MT5_Webhook, id=self.kwargs["pk"])
        if mt5_webhook.hits > mt5_webhook.limit:
            return JsonResponse({"status": "limit exceeded"})
        data = request.data
        tradingview_message = data.get("message")
        params = parse_signal_hit(tradingview_message)
        o = Order.objects.create(
            is_active=True,
            mt5_webhook=mt5_webhook,
            entry=params["entry"],
            sl=params["sl"],
            side=params["side"],
            quantity=params["quantity"]
        )
        o = o.save(commit=False)
        o.mt5_webhook = mt5_webhook
        o.save()


class DiscordAPIView(APIView):
    pass


class EAAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mt5_account = get_object_or_404(MT5_Webhook, webhook_id=self.kwargs["pk"])
        order = Order.objects.filter(is_active=True, mt5_webhook=mt5_account).first()
        if not order:
            return JsonResponse({"status": "no orders"})

        if not order.takeprofit_set.filter(is_active=True).all():
            order.is_active = False
            order.save()
            return JsonResponse({"status": "no orders"})

        tps = order.takeprofit_set.filter(is_active=True).all()
        # make the tp inactive, check if all tps are inactive, and then make the order inactive
        if not tps:
            order.is_active = False
            order.save()
            return JsonResponse({"status": "no orders"})

        tps[0].is_active = False
        tps[0].save()

        # Forward the message to a telegram channel
        # Your code to forward the message to a telegram channel goes here
        return JsonResponse(
            {
                "status": "success",
                "command": "NEW",
                "entry": order.entry,
                "sl": order.sl,
                "tp": tps[0].price,
                "ticker": order.ticker,
                "side": order.side,
                "quantity": order.quantity,
            }
        )
