from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from product.views import ProductListView, ProductDetailView, ReviewCreateView

urlpatterns = [
    path("", ProductListView.as_view(), name="list"),
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
    path("<slug:slug>/review/", ReviewCreateView.as_view(), name="review"),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
