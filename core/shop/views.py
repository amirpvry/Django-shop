from django.shortcuts import render
from django.views.generic import ListView,DetailView
from shop.models import ProductModel, ProductStatusType,ProductCategoryModel

from django.db.models import Q

class ShopProductGrid(ListView):
    model = ProductModel
    paginate_by = 6
    template_name = "shop/product-grid.html"

    def get_queryset(self):
        queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)

        # گرفتن بازه قیمت از پارامترهای URL
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price and max_price:
            queryset = queryset.filter(discounted_price__gte=min_price, discounted_price__lte=max_price)

        # گرفتن پارامتر جستجو
        search_query = self.request.GET.get('q')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # فیلتر بر اساس دسته‌بندی
        category_ids = self.request.GET.getlist('categories')
        if category_ids:
            queryset = queryset.filter(category__id__in=category_ids)
            
        # فیلتر بر اساس سایز
        selected_sizes = self.request.GET.getlist('size')
        if selected_sizes:
            queryset = queryset.filter(size__in=selected_sizes)

        # فیلتر بر اساس ارتباط یا جدیدترین محصولات
        relevance = self.request.GET.get('relevance')
        alphabetical_order = self.request.GET.get('alphabeticalOrder')
        if relevance:
            if relevance == 'mostRecent':
                    queryset = queryset.order_by('-created_date')
            elif relevance == 'lessRecent':
                    queryset = queryset.order_by('created_date')
        elif alphabetical_order:
            if alphabetical_order == 'Z-to-A':
                    queryset = queryset.extra(select={'lower_title': 'LOWER(title)'}).order_by('-lower_title')
            elif alphabetical_order == 'A-to-Z':
                    queryset = queryset.extra(select={'lower_title': 'LOWER(title)'}).order_by('lower_title')


        return queryset


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["total_items"] = self.get_queryset().count()
            context['category'] = ProductCategoryModel.objects.all()

            # اضافه کردن مقادیر بازه قیمت به کانتکست برای نمایش در فرم
            context["min_price"] = self.request.GET.get('min_price', 0)
            context["max_price"] = self.request.GET.get('max_price', 500000)
            return context

    
class ShopProductOverview(DetailView):

    template_name = "shop/product-overview.html"
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
