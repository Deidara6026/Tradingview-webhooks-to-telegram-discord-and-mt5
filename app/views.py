from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import *
from signal_api.models import *
from django.urls import reverse
import requests
from django.conf import settings

# Create your views here.
User = get_user_model()


@login_required
def dashboard(request):
    context = {
        # "signalform":SignalForm(),
        "discord_checkout": checkout("e323c57d-b490-4d15-96fb-00b0ccc1a91c", request.user.id),
        "telegram_checkout": checkout("86a9f6d7-1541-48c9-994a-5c65af3f9c0f", request.user.id),
        "mt5_checkout": checkout("380c7a5a-cab6-445c-af52-733410b62e4c", request.user.id)
    }
    return render(request, "app/dashboard.html", context)


checkout = lambda uid, vid : f"https://stiletto.lemonsqueezy.com/checkout/buy/{vid}?checkout[custom][user_id]={uid}"


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
