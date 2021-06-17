"""
Product Application Views
=========================

"""

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from product.forms import ProductForm
from product.models import Product, Category


class ProductListView(ListView):
    """Product list view implementation"""

    model = Product
    template_name = 'product/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()

        return context


class ProductDetailView(DetailView):
    """Product detail view implementation"""

    model = Product
    extra_context = {"form": ProductForm()}
    template_name = 'product/product_card.html'
