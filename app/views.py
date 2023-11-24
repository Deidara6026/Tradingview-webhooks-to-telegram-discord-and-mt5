from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
 
# Create your views here.
User = get_user_model()


@login_required
def dashboard():

    return render("main/dashboard.html")