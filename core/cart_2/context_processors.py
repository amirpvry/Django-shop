# cart_2/context_processors.py
from .cart import CartSession

def cart_total(request):
    cart = CartSession(request.session)
    total_cart_items = cart.get_cart_total_items()  # تغییر نام متغیر به total_cart_items
    return {
        "total_cart_items": total_cart_items,  # ارسال نام جدید به قالب
    }
