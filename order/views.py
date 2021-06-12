"""
Order Application Views
=======================

"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, )

import json

import order
from order.forms import OrderForm, PurchaseForm, CartEntitiesFormSet
from order.models import Order, OrderCart, OrderItem, Purchase
from product.models import Product


class OrderListView(LoginRequiredMixin, ListView):
    """Order card list view implementation"""

    http_method_names = ["head", "options", "get"]
    model = Order
    template_name = "order/order.html"

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()

        return queryset.filter(customer=self.request.user, is_deleted=False)


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Order card detail view implementation"""

    http_method_names = ["head", "options", "get", "post"]
    model = Order

    def get(self, *args, **kwargs):
        order = self.get_object()
        quantity = Product.objects.get(product=order.product).amount
        if order.customer != self.request.user:
            quantity = quantity - int(order.quantity)
            quantity.save()
            redirect_url = reverse_lazy("order:list")
            return HttpResponseRedirect(redirect_url)

        return super(OrderDetailView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        order = self.get_object()
        quantity = Product.objects.get(product=order.product).amount
        if order.status < Order.CONFIRMED:
            amount = quantity - int(order.quantity)
            amount.save()
            return super(OrderDetailView, self).post(*args, **kwargs)

        redirect_url = order.get_absolute_url()
        return HttpResponseRedirect(redirect_url)


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Order card create view implementation"""

    form_class = OrderForm
    template_name = "order/order_form.html"

    # def get(self, *args, **kwargs):
    #     form = self.form_class(customer=self.request.user)

    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """Order card update view implementation"""

    model = Order
    fields = ["quantity", "address"]

    def get(self, *args, **kwargs):
        order = self.get_object()
        if order.customer != self.request.user:
            redirect_url = reverse_lazy("order:list")
            return HttpResponseRedirect(redirect_url)

        return super(OrderUpdateView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        order = self.get_object()
        if order.status < Order.CONFIRMED:
            return super(OrderUpdateView, self).post(*args, **kwargs)

        redirect_url = order.get_absolute_url()
        return HttpResponseRedirect(redirect_url)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """Order card delete view implementation"""

    model = Order
    success_url = reverse_lazy("order:list")
    template_name = "order/order_confirm.html"

    def get(self, *args, **kwargs):
        order = self.get_object()

        if order.customer != self.request.user:
            redirect_url = reverse_lazy("order:list")
            return HttpResponseRedirect(redirect_url)

        return super(OrderDeleteView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        order = self.get_object()

        if order.status < Order.CONFIRMED:
            order.is_deleted = True
            order.save()
            redirect_url = reverse_lazy("order:list")

        else:
            redirect_url = order.get_absolute_url()

        return HttpResponseRedirect(redirect_url)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = OrderCart.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
    context = {"items": items, "order": order}
    return render(request, 'order/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['fid']
    action = data['action']
    print('Action:', action)
    print('fid:', productId)

    customer = request.user
    product = Product.objects.get(fid=productId)
    orderCart, created = OrderCart.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=orderCart, product=product)

    if action == 'add':
        if orderItem.quantity >= product.amount:
            # raise ValidationError(f"This quantity is not in stock {product.amount}")
             orderItem.quantity = product.amount
        else:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


class CartCheckoutView(CreateView):
    """Cart checkout view implementation"""

    model = Purchase
    template_name = "order/cart.html"
    form_class = PurchaseForm

    def get_cart(self):
        customer = self.request.user
        cart, _ = OrderCart.objects.get_or_create(customer=customer, purchased=False)

        return cart

    def get_cart_entities(self):
        customer = self.request.user
        try:
            cart = OrderCart.objects.get(customer=customer, purchased=False)

            return cart.get_entities()

        except OrderCart.DoesNotExist:

            return OrderCart.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CartCheckoutView, self).get_context_data(**kwargs)

        queryset = self.get_cart_entities()
        cart_entities_formset = CartEntitiesFormSet(queryset=queryset)

        context["formset"] = cart_entities_formset

        return context

    def form_valid(self, form):
        formset = CartEntitiesFormSet(self.request.POST)
        if formset.is_valid():
            formset.save()

        cart = self.get_cart()
        form.instance.cart = cart

        return super(CartCheckoutView, self).form_valid(form)


class PurchaseListView(LoginRequiredMixin, ListView):
    """Purchase list view implementation"""

    model = Purchase

    def get_queryset(self):
        """Return a queryset for a list view"""

        customer = self.request.user
        queryset = Purchase.objects.filter(cart__customer=customer)

        return queryset


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    """Purchase detail view implementation"""

    model = Purchase

    def get(self, request, *args, **kwargs):
        """Handle GET request"""

        customer = request.user
        purchase = self.get_object()

        if customer != purchase.customer:
            raise PermissionDenied

        return super(PurchaseDetailView, self).get(request, *args, **kwargs)


class PurchaseDeleteView(LoginRequiredMixin, DeleteView):
    """Purchase delete view implementation"""

    model = Purchase
    success_url = reverse_lazy("store:list")

    def post(self, request, *args, **kwargs):
        """Handle POST request"""

        purchase = self.get_object()
        threshold = timezone.timedelta(minutes=3)
        if timezone.now() - purchase.purchased_at > threshold:
            raise PermissionDenied

        return super(PurchaseDeleteView, self).post(request, *args, **kwargs)
