from django.urls import path
from .views import signup, log_in, log_out

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('sign-in/', log_in, name='sign-in'),
    path('sign-out/', log_out, name='sign-out'),
]