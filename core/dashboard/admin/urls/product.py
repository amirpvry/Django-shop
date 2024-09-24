from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .. import views



urlpatterns = [
    path('product/list', views.AdminDashboardProductView.as_view() , name = 'product-list'),
    path('product/<int:pk>/edit', views.AdminDashboardProductEditView.as_view() , name = 'product-edit'),
    path('product/create', views.AdminDashboardProductCreateView.as_view() , name = 'product-create'),
    
    path('product/<int:pk>/delete', views.AdminDashboardProductView.as_view() , name = 'product-delete'),
    

]
