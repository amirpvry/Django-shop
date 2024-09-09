from django.urls import path,re_path
from .views import CartProductOverview

app_name = "cart"

urlpatterns = [
    path('', CartProductOverview.as_view(), name='cart'),
]
