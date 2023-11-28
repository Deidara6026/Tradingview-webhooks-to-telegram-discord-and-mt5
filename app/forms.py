from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Signal

class SignalForm(ModelForm):

    class Meta:
        model = Signal
        fields = ["telegram_enabled", "channel_invite_link", "message_prefix", "message_suffix", "mt5_enabled", "mt5_login", "mt5_password", "mt5_server"]
        widgets = {
            "message_prefix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px"}),
            "message_suffix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px"}),
            "telegram_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showtg()", 'checked': True}),
            "mt5_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showmt5()", 'checked': True}),
            "mt5_login": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Login"}),
            "mt5_password": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Password"}),
            "mt5_server": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Server"}),
            "channel_invite_link": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Invite Link"}),

        }