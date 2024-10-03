from django.urls import path,include
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/",views.OrderHomeView.as_view(),name="checkout"),
    path("order_complete/",views.OrderCompleteView.as_view(),name="order_complete"),
    
    

]


