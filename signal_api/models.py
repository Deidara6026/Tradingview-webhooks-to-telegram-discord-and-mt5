from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class TelegramAlert(models.Model):
    channel_invite_link = models.CharField(max_length=25)
    message_format = models.CharField(max_length=500)
    


class Signal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram = models.OneToOneField(TelegramAlert, on_delete=models.CASCADE, null=True, blank=True)
    telegram_enabled = models.BooleanField()
    parse = models.BooleanField()
    