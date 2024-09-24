from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.permissions   import HasAdminAccessPermission
from shop.models import ProductModel, ProductStatusType,ProductCategoryModel
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView,UpdateView,CreateView
from dashboard.admin.forms.product import ProductEditForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse


class AdminDashboardProductView(LoginRequiredMixin, HasAdminAccessPermission,ListView):
    
    

        model = ProductModel
        paginate_by = 100
        template_name = "dashboard/admin/product/product-list.html"

        def get_queryset(self):
            queryset = ProductModel.objects.all()

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
                
                
            price_order = self.request.GET.get('priceOrder')
            if price_order:
                if price_order == 'high-to-low':
                 queryset = queryset.order_by('-discounted_price')
                elif price_order == 'low-to-high':
                 queryset = queryset.order_by('discounted_price')

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

        def post(self, request, *args, **kwargs):
            product_id = kwargs.get('pk')  # گرفتن شناسه محصول برای حذف
            product = ProductModel.objects.get(id=product_id)
            product.delete()  # حذف محصول
            messages.success(request, 'محصول با موفقیت حذف شد.')
            return HttpResponseRedirect(reverse('dashboard:admin:product-list'))
        
        
        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context["total_items"] = self.get_queryset().count()
                context['category'] = ProductCategoryModel.objects.all()

                # اضافه کردن مقادیر بازه قیمت به کانتکست برای نمایش در فرم
                context["min_price"] = self.request.GET.get('min_price', 0)
                context["max_price"] = self.request.GET.get('max_price', 500000)
                return context
            


class AdminDashboardProductEditView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin,UpdateView):
    model = ProductModel  # مدل مربوطه را اضافه کنید

    form_class = ProductEditForm
    template_name = "dashboard/admin/product/product-edit.html"
    # success_url = reverse_lazy('dashboard:admin:product-list')
    success_message = "محصول با موفقیت تغییر کرد."
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-edit', kwargs={'pk': self.object.pk})
    
    
    
class AdminDashboardProductCreateView(LoginRequiredMixin, HasAdminAccessPermission,SuccessMessageMixin,CreateView):
    queryset = ProductModel.objects.all()  # مدل مربوطه را اضافه کنید

    form_class = ProductEditForm
    template_name = "dashboard/admin/product/product-create.html"
    # success_url = reverse_lazy('dashboard:admin:product-list')
    success_message = "پروفایل با موفقیت ایجاد شد."
    
    def get_success_url(self):
        return reverse_lazy('dashboard:admin:product-list')