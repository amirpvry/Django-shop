from .cart import CartSession
from django.shortcuts import redirect,render
from django.views.generic import View , TemplateView
from django.http import JsonResponse
import json


class SessionAddProduct(View):
    
    def post(self,request,*args,**kwargs):
        cart = CartSession(request.session)
        
                # دریافت product_id از درخواست
        data = json.loads(request.body)
        product_id = data.get("product_id")
        
        # اضافه کردن محصول به سبد خرید
        if product_id:
            cart.add_product(product_id)
        # برگرداندن جزئیات سبد خرید به همراه تعداد کل آیتم‌ها
        
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({
            "cart": cart.get_cart_dict(),
            "total_items": cart.get_cart_total_items()  # برگرداندن تعداد کل آیتم‌ها
        })

    def get(self, request, *args, **kwargs):
            # Example of handling GET requests if necessary
            return JsonResponse({"message": "GET requests are not supported for this view."})
        
class SessionUpdateQuantityProductView(View):
    
    def post(self,request,*args,**kwargs):
        cart = CartSession(request.session)
        
        data = json.loads(request.body)
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        
        if product_id and quantity:
            cart.update_product_quantity(product_id,quantity)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({
            "cart": cart.get_cart_dict(),
            "total_items": cart.get_cart_total_items()  # برگرداندن تعداد کل آیتم‌ها
        })
        
class SessionRemoveQuantityProductView(View):

    def post(self, request, *args, **kwargs):
        cart = CartSession(request.session)
        data = json.loads(request.body)
        product_id = data.get("product_id")

        if product_id:
            cart.remove_product(product_id)
        if request.user.is_authenticated:
            cart.merge_session_cart_in_db(request.user)
        return JsonResponse({
            "cart": cart.get_cart_dict(),
            "total_items": cart.get_cart_total_items(),
        })

        
        
class SessionDetailCart(TemplateView):
    template_name = "cart_2/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartSession(self.request.session)
        context['cart'] = cart
        context['total_items'] = cart.get_cart_total_items()  # تعداد کل آیتم‌ها
        context['cart_items'] = cart.get_cart_items()
        context['total_price'] = cart.get_total_price()  
        

        return context
