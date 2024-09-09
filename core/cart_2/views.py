from django.shortcuts import render
from django.views.generic import ListView,DetailView
from shop.models import ProductModel, ProductStatusType,ProductCategoryModel

from django.db.models import Q



class CartProductOverview(DetailView):

    template_name = "cart/cart.html"
    queryset = ProductModel.objects.filter(status=ProductStatusType.publish.value)
