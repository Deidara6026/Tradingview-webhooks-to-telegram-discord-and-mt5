from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt

User = settings.AUTH_USER_MODEL



class Signal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_enabled = models.BooleanField(default=False)
    parse = models.BooleanField(default=False)
    channel_chat_id = models.CharField(max_length=15, null=True)
    message_format = models.CharField(max_length=500, null=True)
    message_prefix = models.CharField(max_length=200, null=True)
    message_suffix = models.CharField(max_length=200, null=True)
    mt5_enabled = models.BooleanField(default=False)
    mt5_login = encrypt(models.CharField(max_length=30, null=True))
    mt5_password = encrypt(models.CharField(max_length=60, null=True))
    mt5_server = encrypt(models.CharField(max_length=30, null=True))