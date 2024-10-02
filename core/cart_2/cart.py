from shop.models import ProductStatusType, ProductModel
from shop.models import ProductModel,ProductStatusType
from cart_2.models import CartModel,CartItemModel

class CartSession:

    total_payment_amount = 0 
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})
        if not isinstance(self._cart, dict):
            self._cart = {"items": []}

    def update_product_quantity(self, product_id, quantity):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                new_quantity = int(quantity)
                if new_quantity > 0:  # چک کردن اینکه موجودی منفی نباشد
                    item["quantity"] = new_quantity  # موجودی را به مقدار جدید تنظیم کنید
                break
        else:
            return 
        self.save()
        
    def remove_product(self, product_id):
        product_id = int(product_id)  # تبدیل به عدد
        for item in self._cart["items"]:
            if product_id == int(item["product_id"]):
                self._cart["items"].remove(item)
                break
        self.save()



    def add_product(self, product_id):
        for item in self._cart["items"]:
            if product_id == item["product_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"product_id": product_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()
        
    def get_cart_dict(self):
        return self._cart
        
    def get_cart_items(self):
        self.total_payment_amount = 0

        cart_items = self._cart.get("items", [])
        
        # اگر سبد خرید خالی باشد، باید لیست خالی برگرداند و ادامه ندهد
        if not cart_items:
            return []
        
        for item in cart_items:
            try:
                # فقط محصولاتی که در سبد خرید هستند فراخوانی می‌شوند
                product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            except ProductModel.DoesNotExist:
                # اگر محصول پیدا نشد، آن را از سبد حذف کنید یا به کاربر اطلاع دهید
                continue
            
            item["product_obj"] = product_obj
            total_price = int(item["quantity"]) * product_obj.calculate_discounted_price()
            item["total_price"] = total_price
            self.total_payment_amount += total_price
        
        return cart_items
            
    def get_total_price(self):
        
        return self.total_payment_amount 
    
    
    def get_cart_total_items(self):
        total_items = 0
        print("Cart contents:", self._cart)  # پرینت محتویات سبد خرید
        items = self._cart.get("items", [])
        print("Items in cart:", items)  # پرینت آیتم‌های موجود در سبد خرید

        for item in items:
            total_items += item.get("quantity", 0)  # جمع‌آوری تعداد آیتم‌ها
        print("Total items calculated:", total_items)  # تعداد آیتم‌ها محاسبه شده

        return total_items  # بازگشت تعداد کل آیتم‌ها

        

    def save(self):
        self.session["cart"] = self._cart  # ذخیره اطلاعات سبد خرید در session
        self.session.modified = True  # نشان دادن اینکه session تغییر کرده است


    def sync_cart_items_from_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.product.id) == item["product_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {"product_id": str(cart_item.product.id), "quantity": cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()
    
            
        
    def merge_session_cart_in_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        
        for item in  self._cart["items"]:
            product_obj = ProductModel.objects.get(id=item["product_id"], status=ProductStatusType.publish.value)
            
            cart_item ,created = CartItemModel.objects.get_or_create(cart=cart,product=product_obj)
            cart_item.quantity = item["quantity"]
            cart_item.save()
        session_product_ids = [item["product_id"] for item in  self._cart["items"]]
        CartItemModel.objects.filter(cart=cart).exclude(product__id__in=session_product_ids).delete()
        
