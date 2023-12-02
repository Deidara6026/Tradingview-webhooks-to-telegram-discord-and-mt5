from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import *
from signal_api.models import SignalWebhook
# Create your views here.
User = get_user_model()


@login_required
def dashboard(request):
    context = {
        "signalform":SignalForm,
        "tg_form": Telegram_Link_Form,
        "mt5_form": MT5_Link_Form, 
        "discord_form": Discord_Link_Form, 
        }
    return render(request, "app/dashboard.html", context)


@login_required
def submit_alert(request):
    if request.method == 'POST':
        data = request.POST
        form = SignalForm(data)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
        # Process the data and display it
        return HttpResponse("Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")
