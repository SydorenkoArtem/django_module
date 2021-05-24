"""
Product Application Views
=========================

"""

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from product.forms import ProductForm
from product.models import Product, Review, Category


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


class ReviewCreateView(CreateView):
    """Review create view implementation"""

    http_method_names = ["post", "head", "options", ]
    model = Review
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy("detail", kwargs={"slug": self.kwargs.get("slug")})

    def form_valid(self, form):
        try:
            product = Product.objects.get(slug=self.kwargs.get("slug"))
            form.instance.product = product

            return super(ReviewCreateView, self).form_valid(form)

        except Product.DoesNotExist:
            return Http404()
