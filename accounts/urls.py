from django.urls import path
from .views import signup, log_in, log_out

urlpatterns = [
    path('sign-up/', signup, name='sign-up'),
    path('login/', log_in, name='login'),
    path('sign-out/', log_out, name='sign-out'),
]