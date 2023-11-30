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

