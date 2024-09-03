from django.shortcuts import render
from django.views.generic import ListView
from shop.models import ProductModel, ProductStatusType

class ShopProductGrid(ListView):
    model = ProductModel
    paginate_by = 6  # تعداد آیتم‌ها در هر صفحه

    template_name = "shop/product-grid.html"
    
    def get_queryset(self):
        # فقط محصولاتی که وضعیت آنها "نمایش" است را فیلتر کنید
        return ProductModel.objects.filter(status=ProductStatusType.publish.value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # تعداد آیتم‌های فیلتر شده (فقط "نمایش" شده‌ها) را بشمارید
        context["total_items"] = self.get_queryset().count()
        return context
    
    
