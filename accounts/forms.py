from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django import forms

from .models import CustomUser

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class":"form-control", 'id':"password1", "placeholder":"Enter Password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"class":"form-control", 'id':"password2", "placeholder":"Confirm Password"}),
    )

    
    class Meta:
        model = CustomUser
        fields = ("username", "email", "phone_no")
        widgets = {
            "username": TextInput(attrs={"class":"form-control", 'id':"userName", "placeholder":"Username"}),
            "email": TextInput(attrs={"class":"form-control", 'id':"email", "placeholder":"Email"}),
            "phone_no": TextInput(attrs={"class":"form-control", 'id':"phoneNumber", "placeholder":"Phone Number"}),
        }

class LogInForm(forms.Form):
    email = forms.EmailField(widget=TextInput(attrs={"class":"form-control", "id":"floatingInput", "placeholder":"name@example.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "id":"Password", "placeholder":"Password"}))