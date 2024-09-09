from django.urls import path,re_path
from .views import ShopProductGrid, ShopProductOverview

app_name = "shop"

urlpatterns = [
    path('product/grid/', ShopProductGrid.as_view(), name='product-grid'),
    re_path(r'^product/(?P<slug>[\w-]+)/product-overview/$', ShopProductOverview.as_view(), name='product-overview'),
]
