from django.urls import path, include
from .views import *

app_name = "shop"

urlpatterns = [
    
    path('product/grid/', ShopProductGrid.as_view(), name='product-grid'),

]