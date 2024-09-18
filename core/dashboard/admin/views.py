from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions   import HasAdminAccessPermission
from dashboard.admin.forms import AdminPasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import FormView
from dashboard.admin.forms import ProfileEditForm
from accounts.models import Profile

from django.urls import reverse_lazy

class AdminDashboardHomeView(LoginRequiredMixin,HasAdminAccessPermission,TemplateView):
    
    template_name= 'dashboard/admin/home.html'
    
    


class AdminSecurityView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, PasswordChangeView):
    form_class = AdminPasswordChangeForm
    template_name = 'dashboard/admin/profile/admin-security.html'
    success_url = reverse_lazy('dashboard:admin:admin-security')
    success_message = "رمز عبور با موفقیت تغییر کرد."

    def form_invalid(self, form):
        messages.error(self.request, "خطایی رخ داد. لطفاً اطلاعات وارد شده را بررسی کنید.")
        return super().form_invalid(form)

class AdminProfileEditView(LoginRequiredMixin, HasAdminAccessPermission, SuccessMessageMixin, FormView):
    form_class = ProfileEditForm
    template_name = 'dashboard/admin/profile/admin-profile-edit.html'
    success_url = reverse_lazy('dashboard:admin:admin-profile-edit')
    success_message = "پروفایل با موفقیت عوض شد"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Profile.objects.get(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
