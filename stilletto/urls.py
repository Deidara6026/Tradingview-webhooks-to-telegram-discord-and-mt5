"""
URL configuration for stilletto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from signal_api.views import TelegramAPIView, MT5APIView, DiscordAPIView, EAAPIView, LemonAPIView
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('dashboard/', dashboard, name="dashboard"),
    path('submittg/', submit_telegram_link, name="submittg"),
    path('submitmt5/', submit_telegram_link, name="submitmt5"),
    path('submitdiscord/', submit_telegram_link, name="submitdiscord"),
    path('tview_api/telegram/<uuid:pk>', TelegramAPIView.as_view(), name="telegram_signal_api_endpoint"),
    path('tview_api/mt5/<uuid:pk>', MT5APIView.as_view(), name="mt5_signal_api_endpoint"),
    path('tview_api/discord/<uuid:pk>', DiscordAPIView.as_view(), name="discord_signal_api_endpoint"),
    path('metatrader_api/<str:pk>', EAAPIView.as_view(), name="ea_signal_api_endpoint"),
    path('webhooks/lemons', LemonAPIView.as_view(), name="lemon_api_endpoint"),
    path('submitalert/', submit_alert, name="submitalert"),

]
