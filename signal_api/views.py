from django.shortcuts import render
from django.http import JsonResponse
from .models import Signal
from .serializers import SignalSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.conf import settings
import telebot
import MetaTrader5 as mt5


def send_telegram_message(message, channel):
    try:
        telegram_settings = settings.TELEGRAM
        bot = telebot.TeleBot(telegram_settings["token"])
        bot.send_message(channel, message)
    except:
        pass

def parse_signal_hit(msg:str):
    if "note:" in msg:
        print("note found")
        note = msg.split("note:")[1]
        msg = msg.split("note:")[0]


    params = msg.split()
    d = {
        'symbol':params[0] if params[0].lower() not in ["buy", "sell", "long", "short"] else params[1],
        'side':params[1] if params[1].lower() in ["buy", "sell", "long", "short"] else params[0]
        }
    for param in params:
        if ":" in param:
            if param.split(':')[0].lower() in ["p", "price"]:
                d.update({'price':param.split(':')[1]})
            if param.split(':')[0].lower() in ["tp"]:
                d.update({'tp':param.split(':')[1]})
            if param.split(':')[0].lower() in ["sl"]:
                d.update({'sl':param.split(':')[1]})
    d.update({'note':note})

    print(d)
    return d

def parse(params:dict, template:str|None=None):
    if template == None:
        template = """
{{side}} {{symbol}}

Entry Price: {{p}}

Take Profit: {{tp}}
Stop Loss: {{sl}}

Comment: {{note}}
        """
    m = template.replace("{{symbol}}", params['symbol'].upper())
    m = m.replace("{{price}}", params['price'])
    m = m.replace("{{p}}", params['price'])
    m = m.replace("{{take profit}}", params['tp'])
    m = m.replace("{{tp}}", params['tp'])
    m = m.replace("{{stop loss}}", params['sl'])
    m = m.replace("{{sl}}", params['sl'])
    m = m.replace("{{side}}", params['side'].upper())
    m = m.replace("{{note}}", params['note'])
    return m

def send_mt5_order(params, det):
    if not mt5.initialize(login=det.mt5_login, server=det.mt5_server, password=det.mt5_password):
        return False
    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": params["symbol"],
    "volume": det.mt5_lot,
    "type": mt5.ORDER_TYPE_BUY if params["side"].lower() in ["buy", "long"] else mt5.ORDER_TYPE_SELL,
    "price": params["price"],
    "sl": params["sl"],
    "tp": params["tp"],
    "deviation": 20,
    "magic": 7776026,
    "comment": "Stilletto Trades",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(request)
    print(result)



class SignalAPIView(APIView):
    def post(self, request, *args, **kwargs):

        signal = Signal.objects.get(id=self.kwargs["pk"])
        data = request.data
        tradingview_message = data.get('message')
        params = parse_signal_hit(tradingview_message)
        if signal.telegram_enabled:
            if signal.parse:
                tradingview_message = parse(params, signal.telegram_template)
            else:
                tradingview_message = parse(params)
            print(tradingview_message)
            send_telegram_message(tradingview_message, signal.channel_chat_id)

        if signal.mt5_enabled:
            pass
        # Forward the message to a telegram channel
        # Your code to forward the message to a telegram channel goes here
        return JsonResponse({'status': 'success'})

