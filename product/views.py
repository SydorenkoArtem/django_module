"""
Product Application Views
=========================

"""

from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from product.forms import ReviewForm
from product.models import Product, Review


class ProductListView(ListView):
    """Product list view implementation"""

    model = Product
    template_name = 'product/product_list.html'


class ProductDetailView(DetailView):
    """Product detail view implementation"""

    model = Product
    extra_context = {"form": ReviewForm()}
    template_name = 'product/product_card.html'


class ReviewCreateView(CreateView):
    """Review create view implementation"""

    http_method_names = ["post", "head", "options", ]
    model = Review
    form_class = ReviewForm

    def get_success_url(self):
        return reverse_lazy("detail", kwargs={"slug": self.kwargs.get("slug")})

    def form_valid(self, form):
        try:
            product = Product.objects.get(slug=self.kwargs.get("slug"))
            form.instance.product = product

            return super(ReviewCreateView, self).form_valid(form)

        except Product.DoesNotExist:
            return Http404()
