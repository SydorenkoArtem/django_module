from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from product.views import ProductListView, ProductDetailView

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
]
