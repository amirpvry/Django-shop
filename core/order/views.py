from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from order.models import UserAddressModel, OrderModel, OrderItemModel, OrderStatusType,CouponModel
from decimal import Decimal
from cart_2.models import CartModel, CartItemModel
from django.urls import reverse_lazy
from django.utils import timezone
from cart_2.cart import CartSession  # برای مدیریت سبد خرید در session
from django.contrib import messages
from .forms import CheckOutForm
class OrderHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'order/checkout.html'
    success_url = reverse_lazy('order:order_complete')

    def calculate_shipping_cost(self, total_price):
        """محاسبه هزینه ارسال."""
        if total_price > 1000000:
            return Decimal(0)
        return Decimal(50000)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(CartModel, user=self.request.user)
        addresses = UserAddressModel.objects.filter(user=self.request.user)
        
        # فرم را به کانتکست اضافه کنید
        context['form'] = CheckOutForm()

        total_price = cart.calculate_total_price()
        shipping_cost = self.calculate_shipping_cost(total_price)
        total_tax = round((total_price * 9) / 100)

        context["total_tax"] = total_tax 
        context["shipping_cost"] = shipping_cost 
        context['total_price'] = total_price + total_tax + shipping_cost
        context["addresses"] = addresses 

        return context

    

    def post(self, request, *args, **kwargs):
        form = CheckOutForm(request.POST)
        if form.is_valid():
            address_id = form.cleaned_data['address_id']
            coupon_code = form.cleaned_data.get('coupon_code', None)

            cart = get_object_or_404(CartModel, user=request.user)
            selected_address = get_object_or_404(UserAddressModel, id=address_id)
            cart_session = CartSession(request.session)

            total_price = cart.calculate_total_price()
            shipping_cost = self.calculate_shipping_cost(total_price)
            total_tax = round((total_price * 9) / 100)
            final_total = total_price + total_tax + shipping_cost

            coupon = None
            if coupon_code:
                try:
                    coupon = CouponModel.objects.get(code=coupon_code, expiration_date__gte=timezone.now())
                    if coupon.used_by.filter(id=request.user.id).exists():
                        messages.error(request, "You have already used this coupon.")
                        return redirect('order:checkout')
                    discount = Decimal(coupon.discount_percent / 100) * final_total
                    final_total -= discount
                except CouponModel.DoesNotExist:
                    messages.error(request, "Invalid or expired coupon.")
                    return redirect('order:checkout')

            # ادامه ثبت سفارش...
            # ساخت سفارش جدید
            order = OrderModel.objects.create(
                user=request.user,
                total_price=final_total,
                status=OrderStatusType.pending,
                address=selected_address,
                state=selected_address.state,
                city=selected_address.city,
                zip_code=selected_address.zip_code,
                coupon=coupon
            )

            # ثبت آیتم‌های سبد خرید به عنوان آیتم‌های سفارش
            cart_items = cart.cart_items.all()
            for item in cart_items:
                OrderItemModel.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.get_price()
                )

            if coupon:
                coupon.used_by.add(request.user)

            # پاک کردن سبد خرید پس از ثبت سفارش
            cart.cart_items.all().delete()
            cart_session.clear()

            return redirect(self.success_url)

        else:
            # اگر فرم نامعتبر بود، مجدداً به صفحه بازگردید و خطاها را نشان دهید
            messages.error(request, "Form is invalid. Please check the details.")
            return self.render_to_response(self.get_context_data())

class OrderCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'order/order-complete.html'
