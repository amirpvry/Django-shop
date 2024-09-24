from django.urls import path,include



app_name = "admin"

urlpatterns = [

    path('', include('dashboard.admin.urls.general')  ),
    path('', include('dashboard.admin.urls.profile')),
    path('', include('dashboard.admin.urls.product')),
    
    # path('admin-profile-image-edit/', views.AdminProfileImageEditView.as_view() , name = 'admin-profile-image-edit'),

]