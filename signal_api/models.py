from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL



class Signal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_enabled = models.BooleanField(default=False)
    parse = models.BooleanField(default=False)
    channel_invite_link = models.CharField(max_length=25, null=True)
    message_format = models.CharField(max_length=500, null=True)
    message_prefix = models.CharField(max_length=200, null=True)
    message_suffix = models.CharField(max_length=200, null=True)
    binance_enabled = models.BooleanField(default=False)
    binance_api_key = models.CharField(max_length=30, null=True)
    binance_api_hash = models.CharField(max_length=30, null=True)