"""
Order Application Views
=======================

"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, )

import json
from order.forms import OrderForm
from order.models import Order, OrderCart, OrderItem
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
            raise ValidationError(f"This quantity is not in stock {product.amount}")
        else:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
