from django.urls import path,include
from .views import *
from . import views

app_name = "admin"

urlpatterns = [
    path('home/', views.AdminDashboardHomeView.as_view() , name = 'home'),
    path('admin-security/', views.AdminSecurityView.as_view() , name = 'admin-security'),
    path('admin-profile-edit/', views.AdminProfileEditView.as_view() , name = 'admin-profile-edit'),

]
