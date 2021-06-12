from django.urls import path


from order.views import OrderUpdateView, OrderDeleteView, OrderListView, OrderDetailView, OrderCreateView, cart, \
    updateItem, PurchaseDetailView, PurchaseDeleteView, PurchaseListView

app_name = "order"


urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("create/", OrderCreateView.as_view(), name="create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", OrderUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", OrderDeleteView.as_view(), name="delete"),
    path("cart/", cart, name="cart"),
    path("update_item/", updateItem, name="update_item"),
    path("<int:pk>/", PurchaseDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", PurchaseDeleteView.as_view(), name="delete"),
    path("", PurchaseListView.as_view(), name="list"),
]
