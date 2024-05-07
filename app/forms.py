from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Telegram_Webhook, Discord_Webhook, MT5_Webhook


class Telegram_Webhook_Form(ModelForm):
    class Meta:
        model = Telegram_Webhook
        fields = ["name", "message_prefix", "message_suffix", "parse", "message_format"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Webhook Name",
                }
            ),
            "message_prefix": Textarea(
                attrs={
                    "placeholder": "Message Prefix: Optional text placed before all your telegram alerts. Greet your followers maybe?",
                    "style": "width: 70%;height:120px;",
                }
            ),
            "message_suffix": Textarea(
                attrs={
                    "placeholder": "Message Prefix: Optional text placed after all your telegram alerts. Greet your followers maybe?",
                    "style": "width: 70%;height:120px;",
                }
            ),
            "parse": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "onclick": "show_tg_parse()",
                    "checked": False,
                }
            ),
            "message_format": Textarea(
                attrs={
                    "placeholder": "Message Prefix: Optional text placed after all your telegram alerts. Greet your followers maybe?",
                    "style": "width: 70%;height:120px;",
                }
            ),
            # "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }


class Discord_Webhook_Form(ModelForm):
    class Meta:
        model = Discord_Webhook
        fields = ["name", "message_prefix", "message_suffix", "parse", "message_format"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Webhook Name",
                }
            ),
            "message_prefix": Textarea(
                attrs={
                    "placeholder": "Message Prefix: Optional text placed before all your discord alerts. Greet your followers maybe?",
                    "style": "width: 70%;height:120px;",
                }
            ),
            "message_suffix": Textarea(
                attrs={
                    "placeholder": "Message Prefix: Optional text placed after all your discord alerts. Greet your followers maybe?",
                    "style": "width: 70%;height:120px;",
                }
            ),
            "parse": CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "onclick": "show_tg_parse()",
                    "checked": False,
                }
            ),
            # "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }


class MT5_Webhook_Form(ModelForm):
    class Meta:
        model = MT5_Webhook
        fields = ["name"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name...",
                    "style": "border-color:#766e61;",
                }
            ),
        }
