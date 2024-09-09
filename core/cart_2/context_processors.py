def cart_total(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())  # جمع تعداد تمام محصولات در سبد
    
    return {'cart_total_items': total_items}
