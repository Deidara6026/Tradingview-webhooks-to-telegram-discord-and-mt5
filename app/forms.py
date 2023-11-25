from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Signal

class SignalForm(ModelForm):

    class Meta:
        model = Signal
        fields = ["telegram_enabled", "channel_invite_link", "message_prefix", "message_suffix", "binance_enabled", "binance_api_key", "binance_api_hash"]
        widgets = {
            "message_prefix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px"}),
            "message_suffix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px"}),
            "telegram_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showtg()", 'checked': True}),
            "binance_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showbinance()", 'checked': True}),
            "binance_api_key": TextInput(attrs={"class":"form-control", "placeholder":"Binance Api Key"}),
            "binance_api_hash": TextInput(attrs={"class":"form-control", "placeholder":"Binance Api Hash"}),
            "channel_invite_link": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Invite Link"}),

        }