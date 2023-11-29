from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from .forms import *
from signal_api.models import Signal
# Create your views here.
User = get_user_model()


@login_required
def dashboard(request):
    signals = Signal.objects.filter(user=request.user).all()
    d = []
    for signal in signals:
        d.append({
            "id":signal.id, 
            "channel_invite_link":signal.channel_chat_id, 
            "telegram_enabled":signal.telegram_enabled, 
            "binance_enabled":signal.mt5_enabled, 
            "mp":signal.message_prefix,
            "ms":signal.message_suffix,  
        })
    context = {"signalform":SignalForm, "signals":d}
    print(signals)
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
