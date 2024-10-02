from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from order.permissions import HasCustomerAccessPermission
from order.models import UserAddressModel, OrderModel, CouponModel ,OrderStatusType # فرض بر این است که این مدل‌ها موجود هستند
from decimal import Decimal
from cart_2.models import CartModel


class OrderHomeView(LoginRequiredMixin, HasCustomerAccessPermission, TemplateView):
    
    template_name = 'order/checkout.html'
    
    def calculate_shipping_cost(self, total_price):
        """محاسبه هزینه ارسال. می‌توانید این تابع را با توجه به نیاز خود تغییر دهید"""
        if total_price > 100000:  # فرض کنید اگر قیمت بیشتر از یک مقدار خاص باشد، ارسال رایگان است
            return Decimal(0)
        return Decimal(50000)  # فرض کنید هزینه ارسال ثابت است
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            cart = CartModel.objects.get(user=self.request.user)
        except CartModel.DoesNotExist:
            cart = None
            context["total_price"] = 0
            context["total_tax"] = 0
            context["shipping_cost"] = 0  # اگر سبد خرید خالی باشد، هزینه ارسال 0 است

        else:
            total_price = cart.calculate_total_price()
            
           
            tax=round((total_price * 9) / 100)  # نرخ مالیات ثابت 9%
            context["total_price"] = total_price + tax
            context["total_tax"] = tax
            
            shipping_cost = self.calculate_shipping_cost(total_price)
            context["shipping_cost"] = shipping_cost
        # اضافه کردن آدرس‌های کاربر به context
        context["addresses"] = UserAddressModel.objects.filter(user=self.request.user)

        return context
