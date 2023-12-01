from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django import forms

from .models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_no")
        widgets = {
            "username": TextInput(attrs={"class":"form-control"}),
            "email": TextInput(attrs={"class":"form-control"}),
            "phone_no": TextInput(attrs={"class":"form-control"}),
        }

class LogInForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))