from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt

User = settings.AUTH_USER_MODEL



class SignalWebhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_extra = models.BooleanField(default=False)
    daily_limit = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    

class MT5_Link(models.Model):
    webhook = models.ForeignKey(SignalWebhook, on_delete=models.CASCADE)
    mt5_login = encrypt(models.CharField(max_length=30, null=True, blank=True))
    mt5_password = encrypt(models.CharField(max_length=60, null=True, blank=True))
    mt5_server = encrypt(models.CharField(max_length=30, null=True, blank=True))
    mt5_lot = models.FloatField(null=True, blank=True)

class Telegram_Link(models.Model):
    webhook = models.ForeignKey(SignalWebhook, on_delete=models.CASCADE)
    parse = models.BooleanField(default=False)
    channel_chat_id = models.CharField(max_length=15, null=True, blank=True)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)

class Discord_Link(models.Model):
    webhook = models.ForeignKey(SignalWebhook, on_delete=models.CASCADE)
    parse = models.BooleanField(default=False)
    channel_chat_id = models.CharField(max_length=15, null=True, blank=True)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)