from django import template
from django.template import loader
from shop.models import ProductModel, ProductStatusType,ProductCategoryModel

register = template.Library()

@register.inclusion_tag('includes/latest_product.html')
def my_custom_tag():

    latest_product = ProductModel.objects.filter(status=ProductStatusType.publish.value).order_by('-created_date')[:8]

    return {"latest_product":latest_product}

@register.inclusion_tag('includes/similar_product.html')
def similar_products_tag(product_id):
    product = ProductModel.objects.get(id=product_id)
    
    # فیلتر محصولات مشابه بر اساس دسته‌بندی‌ها
    similar_product = ProductModel.objects.filter(
        status=ProductStatusType.publish.value,
        category__in=product.category.all()  # بررسی دسته‌بندی‌های مرتبط
    ).exclude(id=product_id).order_by('-created_date')[:8]
    
    return {"similar_product": similar_product}
