from django.urls import path,include

from .. import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('admin-security/', views.AdminSecurityView.as_view() , name = 'admin-security'),
    path('admin-profile-edit/', views.AdminProfileEditView.as_view() , name = 'admin-profile-edit'),
    # path('admin-profile-image-edit/', views.AdminProfileImageEditView.as_view() , name = 'admin-profile-image-edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)