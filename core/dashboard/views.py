from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import UserType
from django.urls import reverse_lazy



class DashboardHomeView(LoginRequiredMixin, View):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.type == UserType.customer.value:
                return redirect(reverse_lazy('dashboard:customer:home'))  # آدرس مقصد را تغییر دهید
            # if request.user.type == UserType.superuser.value:
            #     return redirect(reverse_lazy('dashboard:superuser:home'))  # آدرس مقصد را تغییر دهید
            if request.user.type == UserType.admin.value:
                return redirect(reverse_lazy('dashboard:admin:home'))  # آدرس مقصد را تغییر دهید
            
        else:
            return redirect(reverse_lazy('account:login'))

        return super().dispatch(request, *args, **kwargs)

    