from django.urls import path,include
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/",views.OrderHomeView.as_view(),name="checkout"),
    

]


