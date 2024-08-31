from django.contrib.auth import views as auth_views
from accounts.forms import CustomAuthenticationForm
from django.shortcuts import render
# Custom Login View
class LoginView(auth_views.LoginView):
   
    template_name = "accounts/login.html"
    redirect_authenticated_user = False
    form_class = CustomAuthenticationForm


def custom_404_view(request, exception=None):
    return render(request, 'error_template.html', {
        'error_title': 'Page Not Found',
        'error_message': 'The page you are looking for does not exist.',
    }, status=404)
