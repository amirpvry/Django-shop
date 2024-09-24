from django import forms
from django.contrib.auth.views import PasswordChangeView
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from shop.models import ProductModel,ProductCategoryModel


        
class ProductEditForm(forms.ModelForm):
    
    category = forms.ModelMultipleChoiceField(
    queryset=ProductCategoryModel.objects.all(),
    widget=forms.CheckboxSelectMultiple,  # یا forms.SelectMultiple برای ظاهر دراپ‌داون
    required=True
    )
    
    class Meta:
        model = ProductModel
        fields = [
            "user",
            "category",
            "title",
            "status",
            "slug",
            "image",
            "description",
            "brief_description",
            "stock",
            "price",
            "discount_percent",
            "avg_rate",
            "size",
        ]
        
