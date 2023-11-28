from rest_framework import serializers
from .models import Signal


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ["telegram_enabled", "channel_invite_link", "message_prefix", "message_suffix", "mt5_enabled", "mt5_login", "mt5_password", "mt5_server","user"]