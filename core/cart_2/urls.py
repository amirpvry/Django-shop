from django.urls import path
from . import views

app_name = "cart_2"  # This defines the app name for namespacing

urlpatterns = [
    path('session/add-product', views.SessionAddProduct.as_view(), name='session-add-product'),
    path('session/update/quantity-product', views.SessionUpdateQuantityProductView.as_view(), name='session-update-quantity-product'),
    path('session/remove/quantity-product', views.SessionRemoveQuantityProductView.as_view(), name='session-remove-quantity-product'),

    path('session/detail-cart', views.SessionDetailCart.as_view(), name='session-detail-cart'),

 
]
