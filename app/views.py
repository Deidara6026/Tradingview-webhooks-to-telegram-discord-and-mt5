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

def pricing(request):
    return render(request, "app/pricing.html")


@login_required
def dashboard(request):
    discord_list = Discord_Webhook.objects.filter(user=request.user).prefetch_related("discordchat_set").all()
    telegram_list = Telegram_Webhook.objects.filter(user=request.user).prefetch_related("telegramchat_set").all()
    mt5_list = MT5_Webhook.objects.filter(user=request.user).all()
    orders = Order.objects.filter(user=request.user).order_by("-id").prefetch_related("takeprofit_set").all()[:100]
    webhooks = list(mt5_list) + list(discord_list) + list(telegram_list)
    print(orders)
    
    context = {
        "webhooks": webhooks,
        "orders": orders,
        "range":range(20),

        "telegram_form": Telegram_Webhook_Form(),
        "discord_form": Discord_Webhook_Form(),
        "mt5_form": MT5_Webhook_Form(),
        # "myjournal_form": Telegram_Webhook_Form(),
        "customer_portal": "https://stiletto.lemonsqueezy.com/billing",
        "discord_checkout": checkout(request.user.id, "e323c57d-b490-4d15-96fb-00b0ccc1a91c"),
        "telegram_checkout": checkout(request.user.id, "86a9f6d7-1541-48c9-994a-5c65af3f9c0f"),
        "mt5_checkout": checkout(request.user.id, "380c7a5a-cab6-445c-af52-733410b62e4c")
    }

    return render(request, "app/dashboard.html", context)


@login_required
def toggle_webhook_status(request, webhook_id, identifier):
    # Attempt to retrieve the appropriate webhook with the given id that belongs to the current user based on the identifier
    
    if identifier == "tg":
        webhook = Telegram_Webhook.objects.filter(pk=webhook_id, user=request.user).first()
    elif identifier == "discord":
        webhook = Discord_Webhook.objects.filter(pk=webhook_id, user=request.user).first()
    elif identifier == "mt5":
        webhook = MT5_Webhook.objects.filter(pk=webhook_id, user=request.user).first()
    else:
        webhook = None
    
    if not webhook:
        return HttpResponse("Webhook not found.", status=404)
    
    # Toggle the status of the webhook
    if webhook.pause == 'active':
        webhook.pause = 'inactive'
    else:
        webhook.pause = 'active'
    
    # Save the updated webhook
    webhook.save()
    
    return HttpResponse(f"Webhook status changed to {webhook.pause}.", status=200)

@login_required
def get_webhook_form(request, webhook_id, identifier):
    # Determine the model based on the identifier and retrieve the instance
    if identifier == "tg":
        model = Telegram_Webhook
        form_class = Telegram_Webhook_Form
    elif identifier == "discord":
        model = Discord_Webhook
        form_class = Discord_Webhook_Form
    elif identifier == "mt5":
        model = MT5_Webhook
        form_class = MT5_Webhook_Form
    else:
        return JsonResponse({"error": "Invalid identifier"}, status=400)

    # Retrieve the webhook instance
    webhook = model.objects.filter(pk=webhook_id, user=request.user).first()
    if not webhook:
        return JsonResponse({"error": "Webhook not found"}, status=404)

    # Generate the form with the instance
    form = form_class(instance=webhook)

    # Render form as HTML
    form_html = render_to_string('app/webhook_form.html', {'form': form}, request=request)

    return JsonResponse({"form": form_html}, status=200)


@login_required
def submit_telegram_webhook(request):
    if request.method == "POST":
        data = request.POST
        form = Telegram_Webhook_Form(data)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponse("Webhook data received and processed successfully")
        else:
            return HttpResponse("Invalid form data. Please check your input.")
    else:
        return HttpResponse("Only POST requests are allowed")

@login_required
def submit_mt5_webhook(request):
    if request.method == "POST":
        data = request.POST
        form = MT5_Webhook_Form(data)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponse("Webhook data received and processed successfully")
        else:
            return HttpResponse("Invalid form data. Please check your input.")
    else:
        return HttpResponse("Only POST requests are allowed")

@login_required
def submit_discord_webhook(request):
    if request.method == "POST":
        data = request.POST
        form = Discord_Webhook_Form(data)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return HttpResponse("Webhook data received and processed successfully")
        else:
            return HttpResponse("Invalid form data. Please check your input.")
    else:
        return HttpResponse("Only POST requests are allowed")



# @login_required
# def dashboard(request):
#     # Get the webhooks that the user has, serialize for json, and add to webpage context
#     discord_list = Discord_Webhook.objects.filter(user=request.user).all()
#     telegram_list = Telegram_Webhook.objects.filter(user=request.user).all()
#     mt5_list = MT5_Webhook.objects.filter(user=request.user).all()
#     last_week_alerts = Alert.objects.filter(webhook__user=request.user, date__gte=datetime.datetime.today()-datetime.timedelta(days=7)) # Finish this shit... lol
#     now = datetime.datetime.now()
#     l = []
#     for x in range(7):
#         d = now - datetime.timedelta(days=x)
#         l.append(int(d.strftime("%d")))
#     last_week_dict = dict.fromkeys(l, 0)
#     print(last_week_dict)
#     for alert in last_week_alerts:
#         d = alert.date.strftime("%d")
#         try:
#             last_week_dict[int(d)] += 1
#         except KeyError:
#             continue
#     print(last_week_alerts)
#     orders=[]
#     if mt5_list:
#         orders = Order.objects.order_by("-id").filter(reduce(lambda x,y : x | y, [Q(literal_webhook_id=webhook.webhook_id) for webhook in mt5_list]))[:10]

#     webhooks= list(mt5_list)+list(discord_list)+list(telegram_list),
#     lv = list(last_week_dict.values())
#     lv.reverse()
#     order_list = []
#     for order in orders:
#         order_list.append([order, 1, ", ".join([str(tp.price) for tp in order.takeprofit_set.all()]), order.literal_webhook_id])
#     print(webhooks)
#     context = {
#         # "signalform":SignalForm(),
#         "orders": order_list,
#         "last_week_len": len(last_week_alerts),
#         "last_week_y": lv,
#         "last_week_keys": l,
#         "webhooks": webhooks[0],
#         "webhook_len": len(webhooks),
#         "last_week_alerts": last_week_alerts,
#         "username": request.user.username,
#         "discord_checkout": checkout("e323c57d-b490-4d15-96fb-00b0ccc1a91c", request.user.id),
#         "telegram_checkout": checkout("86a9f6d7-1541-48c9-994a-5c65af3f9c0f", request.user.id),
#         "mt5_checkout": checkout("380c7a5a-cab6-445c-af52-733410b62e4c", request.user.id)
#     }
#     return render(request, "app/dashboard.html", context)


checkout = lambda uid, vid : f"https://stiletto.lemonsqueezy.com/buy/{vid}?checkout[custom][user_id]={uid}"


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
def add_chat(request):
    # Get the data from the POST request
    data = request.POST
    print(data)
    pk = data.get('editmodalwid')
    identifier = data.get('editmodalw')
    chat_id = dict([item.split(":") for item in data.getlist('chat_id')])
    parse = data.get('parse', False)
    message_prefix = data.get('message-prefix')
    message_suffix = data.get('message-suffix')
    name = data.get('name')
    print(chat_id)
    # Determine the model based on the identifier
    if identifier == "tg":
        webhook = Telegram_Webhook.objects.filter(pk=pk, user=request.user).first()
        webhook.parse = parse
        webhook.message_prefix = message_prefix
        webhook.message_suffix = message_suffix
        webhook.name = name
        webhook.save()
        for before in chat_id.keys():
            if webhook.telegramchat_set.filter(chat_id=before).exists():
                telegram_chat = webhook.telegramchat_set.get(chat_id=before)
                telegram_chat.chat_id = chat_id[before]
                telegram_chat.save()
            else:
                if webhook.chat_limit > len(webhook.telegramchat_set.all()):
                    c = TelegramChat.objects.create(webhook=webhook, chat_id=chat_id[before])
                    c.save()
    elif identifier == "discord":
        webhook = Discord_Webhook.objects.filter(pk=pk, user=request.user).first()
        webhook.parse = parse
        webhook.message_prefix = message_prefix
        webhook.message_suffix = message_suffix
        webhook.name = name
        webhook.save()
        for before in chat_id.keys():
            if webhook.discordchat_set.filter(channel_webhook_url=before).exists():
                discord_chat = webhook.discordchat_set.get(channel_webhook_url=before)
                discord_chat.channel_webhook_url = chat_id[before]
                discord_chat.save()
            else:
                if webhook.chat_limit > len(webhook.discordchat_set.all()):
                    c = DiscordChat.objects.create(webhook=webhook, channel_webhook_url=chat_id[before])
                    c.save()
    else:
        return redirect('dashboard', error="An error occured, please reload the page and try again.")
    
    # Save the chat
   
    
    return redirect('dashboard', message="Chat added Successfully!")



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
        return redirect("dashboard","Data received and processed successfully")
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
        return redirect("dashboard","Data received and processed successfully")
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
        return redirect("dashboard","Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")


@login_required
def delete_webhook(request, webhook_id, identifier):
    # Determine the model based on the identifier
    if identifier == "tg":
        model = Telegram_Webhook
    elif identifier == "discord":
        model = Discord_Webhook
    elif identifier == "mt5":
        model = MT5_Webhook
    else:
        return redirect('dashboard', error="An error occured, please reload the page and try again.")

    # Retrieve the webhook instance
    webhook = model.objects.filter(pk=webhook_id, user=request.user).first()
    if not webhook:
        return redirect('dashboard', error="An error occured, please reload the page and try again.")
    # Get the subscription_id from the webhook
    subscription_id = webhook.subscription_id

    # Send a request to lemonsqueezy to stop recurring payments
    lemonsqueezy_url = "https://api.lemonsqueezy.com/subscriptions/{}/cancel".format(subscription_id)
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {settings.LEMONSQUEEZY['api_key']}",
    }
    response = requests.post(lemonsqueezy_url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        return redirect('dashboard', error="Failed to cancel recurring payment, Please try again.")
    # Delete the webhook and its related child objects
    webhook.delete()

    return redirect("dashboard",message="Webhook and all related data have been deleted successfully.")

