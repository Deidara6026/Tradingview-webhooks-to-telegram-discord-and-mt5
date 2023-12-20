from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

User = settings.AUTH_USER_MODEL



class Alert(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

class MT5_Webhook(models.Model):
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)  
    mt5_id = models.UUIDField(default=uuid.uuid4, editable=False)  
    subscription_id = models.CharField(max_length=15, null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    meta_id = models.UUIDField(default=uuid.uuid4, editable=False)
    hit_limit = models.IntegerField()
    hits = models.IntegerField()
    old_alerts = GenericRelation(Alert)


class Order(models.Model):
    is_active = models.BooleanField()
    mt5_webhook = models.ForeignKey(MT5_Webhook, on_delete=models.CASCADE)
    entry = models.FloatField()
    sl = models.FloatField()
    side = models.CharField(max_length=5)
    quantity = models.FloatField()
    ticker = models.CharField(max_length=10, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)



class TakeProfit(models.Model):
    price = models.FloatField()
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Telegram_Webhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    # update_payment_method = models.CharField(max_length=50, null=True, blank=True)
    webhook_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    parse = models.BooleanField(default=False)
    hits = models.IntegerField()
    hit_limit = models.IntegerField()
    chat_limit = models.IntegerField()
    old_alerts = GenericRelation(Alert)
    status = models.CharField(max_length=10)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)


class TelegramChat(models.Model):
    chat_id = models.CharField(max_length=20)
    webhook = models.ForeignKey(Telegram_Webhook, on_delete=models.CASCADE)


class Discord_Webhook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    subscription_id = models.UUIDField(null=True, blank=True)
    product_id = models.UUIDField(null=True, blank=True)
    variant_id = models.UUIDField(null=True, blank=True)
    renews_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    parse = models.BooleanField(default=False)
    hits = models.IntegerField(null=True, blank=True)
    limit = models.IntegerField(null=True, blank=True)
    old_alerts = GenericRelation(Alert)
    message_format = models.CharField(max_length=500, null=True, blank=True)
    message_prefix = models.CharField(max_length=200, null=True, blank=True)
    message_suffix = models.CharField(max_length=200, null=True, blank=True)

class DiscordChat(models.Model):
    channel_webhook_url = models.CharField(max_length=200)
    webhook = models.ForeignKey(Discord_Webhook, on_delete=models.CASCADE)