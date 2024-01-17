from django.forms import ModelForm, Textarea, TextInput, CheckboxInput
from signal_api.models import Telegram_Webhook, Discord_Webhook, MT5_Webhook 



class Telegram_Webhook_Form(ModelForm):
    class Meta:
        model = Telegram_Webhook
        fields = [ "message_prefix", "message_suffix","parse", "message_format"]
        widgets = {
            "message_prefix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "message_suffix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "parse": CheckboxInput(attrs={"class":"form-check-input", "onclick":"show_tg_parse()", 'checked': False}),
            # "channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Telegram Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }
class Discord_Webhook_Form(ModelForm):
    class Meta:
        model = Discord_Webhook
        fields = [ "message_prefix", "message_suffix","parse", "message_format"]
        widgets = {
            "message_prefix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "message_suffix": Textarea(attrs={"placeholder":"Message Prefix(optional)", "style":"width: 90%;height:120px;background-color: #131516; color: aliceblue;border-color:#766e61;"}),
            "parse": CheckboxInput(attrs={"class":"form-check-input", "onclick":"show_tg_parse()", 'checked': False}),
            #"channel_chat_id": TextInput(attrs={"class":"form-control", "placeholder":"Discord Chat ID", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
        }
# class MT5_Webhook_Form(ModelForm):
#     class Meta:
#         model = MT5_Webhook
#         fields = ["mt5_login", "mt5_password", "mt5_server", "mt5_lot"]
#         widgets = {
#             "mt5_login": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Login", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
#             "mt5_password": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Password", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
#             "mt5_lot": TextInput(attrs={"class":"form-control", "placeholder":"Position Size(lot size)", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
#             "mt5_server": TextInput(attrs={"class":"form-control", "placeholder":"mt5 Server", "style":"background-color: #131516; color: aliceblue;border-color:#766e61;"}),
#         }
