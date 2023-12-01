from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Signal

class SignalForm(ModelForm):

    class Meta:
        model = Signal
        fields = ["telegram_enabled", "channel_chat_id", "message_prefix", "message_suffix", "mt5_enabled", "mt5_login", "mt5_password", "mt5_server", "mt5_lot"]
        widgets = {
            "message_prefix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "message_suffix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "telegram_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showtg()", 'checked': True}),
            "mt5_enabled": CheckboxInput(attrs={"class":"form-check-input", "onclick":"showmt5()", 'checked': True}),
            "mt5_login": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Login", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "mt5_password": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Password", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "mt5_lot": TextInput(attrs={"class":"form-control", "placeholder":"Position Size(lot size)", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "mt5_server": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Server", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),

        }