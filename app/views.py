from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import *
from signal_api.models import *
from django.urls import reverse
import requests
from django.conf import settings
from django.db.models import Q
from functools import reduce
import datetime

# Create your views here.
User = get_user_model()


def index(request):
    return render(request, "app/home.html")

def platforms(request):
    return render(request, "app/platforms.html")

@login_required
def dashboard(request):
    # Get the webhooks that the user has, serialize for json, and add to context
    discord_list = Discord_Webhook.objects.filter(user=request.user).all()
    telegram_list = Telegram_Webhook.objects.filter(user=request.user).all()
    mt5_list = MT5_Webhook.objects.filter(user=request.user).all()
    last_week_alerts = Alert.objects.filter(webhook__user=request.user) # Finish this shit
    now = datetime.datetime.now()
    l = []
    for x in range(7):
        d = now - datetime.timedelta(days=x)
        l.append(int(d.strftime("%d")))
    last_week_dict = dict.fromkeys(l, 0)

    for alert in last_week_alerts:
        d = alert.date.strftime("%d")
        last_week_dict[int(d)] += 1
    print(last_week_alerts)
    orders=[]
    if mt5_list:
        orders = Order.objects.order_by("-id").filter(reduce(lambda x,y : x | y, [Q(mt5_webhook=webhook) for webhook in mt5_list]))[:10]

    webhooks= list(mt5_list)+list(discord_list)+list(telegram_list),
    lv = list(last_week_dict.values())
    lv.reverse()
    order_list = []
    for order in orders:
        order_list.append([order,order.mt5_webhook.name, ", ".join([str(tp.price) for tp in order.takeprofit_set.all()])])
    print(webhooks)
    context = {
        # "signalform":SignalForm(),
        "orders": order_list,
        "last_week_len": len(last_week_alerts),
        "last_week_y": lv,
        "last_week_keys": l,
        "webhooks": webhooks[0],
        "webhook_len": len(webhooks),
        "last_week_alerts": last_week_alerts,
        "username": request.user.username,
        "discord_checkout": checkout("e323c57d-b490-4d15-96fb-00b0ccc1a91c", request.user.id),
        "telegram_checkout": checkout("86a9f6d7-1541-48c9-994a-5c65af3f9c0f", request.user.id),
        "mt5_checkout": checkout("380c7a5a-cab6-445c-af52-733410b62e4c", request.user.id)
    }
    return render(request, "app/dashboard.html", context)


checkout = lambda uid, vid : f"https://stiletto.lemonsqueezy.com/checkout/buy/{vid}?checkout[custom][user_id]={uid}&checkout[custom][vid]={vid}"


@login_required
def submit_alert(request):
    if request.method == "POST":
        form = 1  # SignalForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            response = {
                "name": form.name,
                "link": f"{reverse('signal_api_endpoint')}/{form.id}",
                "id": form.id,
            }
            return JsonResponse(response)


@login_required
def submit_telegram_link(request, pk):
    if request.method == "POST":
        data = request.POST
        form = Telegram_Link_Form(data)
        if form.is_valid:
            form = form.save(commit=False)
            form.webhook = SignalWebhook.objects.get(id=pk)
            form.save()
        # Process the data and display it
        return HttpResponse("Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")


@login_required
def submit_mt5_link(request, pk):
    if request.method == "POST":
        data = request.POST
        form = MT5_Link_Form(data)
        if form.is_valid:
            form = form.save(commit=False)
            form.webhook = SignalWebhook.objects.get(id=pk)
            form.save()
        # Process the data and display it
        return HttpResponse("Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")


@login_required
def submit_discord_link(request, pk):
    if request.method == "POST":
        data = request.POST
        form = Discord_Link_Form(data)
        if form.is_valid:
            form = form.save(commit=False)
            form.webhook = SignalWebhook.objects.get(id=pk)
            form.save()
        # Process the data and display it
        return HttpResponse("Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")
