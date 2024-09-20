from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .. import views



urlpatterns = [
    path('home/', views.AdminDashboardHomeView.as_view() , name = 'home'),

    # path('admin-profile-image-edit/', views.AdminProfileImageEditView.as_view() , name = 'admin-profile-image-edit'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)