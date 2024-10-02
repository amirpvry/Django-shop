from django.db import models

# Create your models here.
class CartModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.email
    def calculate_total_price(self):
        # جمع کردن کل قیمت همه آیتم‌ها در سبد خرید
        return sum(item.get_total_price() for item in self.cart_items.all())
    
class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel,on_delete=models.CASCADE,related_name="cart_items") 
    product = models.ForeignKey('shop.ProductModel',on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

        
    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"
    def get_total_price(self):
        product_price = self.product.get_price()  # متد get_price برای محاسبه قیمت محصول
        return product_price * self.quantity  # قیمت کل با توجه به تعداد محصول
