from django.urls import path
from .views import LoginView
from django.conf.urls import handler404
from .views import custom_404_view

app_name = "accounts"



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]


handler404 = custom_404_view
