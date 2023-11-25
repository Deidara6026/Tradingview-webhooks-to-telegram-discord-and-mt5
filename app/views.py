from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
 
# Create your views here.
User = get_user_model()


@login_required
def dashboard(request):
    context = {"signalform":SignalForm}
    return render(request, "app/dashboard.html", context)


@login_required
def submit_alert(request):
    if request.method == 'POST':
        data = request.POST
        form = SignalForm(data)
        if form.is_valid:
            form = form.save(commit=False)
            form.user = request.user
            form.save()
        # Process the data and display it
        return HttpResponse("Data received and processed successfully")
    else:
        return HttpResponse("Only POST requests are allowed")
