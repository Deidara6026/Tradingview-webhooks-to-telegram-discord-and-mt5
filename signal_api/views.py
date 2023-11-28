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



class SignalAPIView(APIView):
    def post(self, request, _id):
        signal = Signal.objects.get(id=_id)
        data = request.data
        tradingview_message = data.get('message')
        if signal.telegram_enabled:
            if signal.parse:
                tradingview_message = parse(tradingview_message, signal.parse)
            send_telegram_message(tradingview_message, signal.channel_chat_id)
        # Forward the message to a telegram channel
        # Your code to forward the message to a telegram channel goes here
        return JsonResponse({'status': 'success'})

