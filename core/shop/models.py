from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


class ProductStatusType(models.IntegerChoices):
    publish = 1 ,("نمایش")
    draft = 2 ,("عدم نمایش")


class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
        
    def __str__(self):
        return self.title
    


# Create your models here.
class ProductModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    category = models.ManyToManyField(ProductCategoryModel)
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique=True)
    image = models.ImageField(default="/default/product-image.png",upload_to="product/img/")
    description = models.TextField()
    brief_description = models.TextField(null=True,blank=True)
    
    stock = models.PositiveIntegerField(default=0)
    status = models.IntegerField(choices=ProductStatusType.choices,default=ProductStatusType.draft.value)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=0)
    discount_percent = models.IntegerField(default=0,validators = [MinValueValidator(0),MaxValueValidator(100)])
    discounted_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)  # فیلد جدید

    avg_rate = models.FloatField(default=0.0)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'XLarge'),
        ('XXL', 'XXLarge'),
        

    ]
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')

    class Meta:
        ordering = ["-created_date"]
        
    def __str__(self):
        return self.title
    
    def calculate_discounted_price(self):
        """محاسبه قیمت نهایی پس از تخفیف به صورت عددی"""
        if self.discount_percent > 0:
            discount_amount = self.price * (Decimal(self.discount_percent) / 100)
            discount_amount = round(discount_amount)
            return self.price - discount_amount
        return self.price


    def save(self, *args, **kwargs):
        """Override the save method to calculate discounted_price before saving."""
        self.discounted_price = self.calculate_discounted_price()
        super().save(*args, **kwargs)  # Call the "real" save() method.
        



    def is_discounted(self):
        return self.discount_percent != 0
    
    def is_published(self):
        return self.status == ProductStatusType.publish.value
    
class ProductImageModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name="product_images")
    file = models.ImageField(upload_to="product/extra-img/")
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_date"]
        
class WishlistProductModel(models.Model):
    user = models.ForeignKey("accounts.User",on_delete=models.PROTECT)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.title