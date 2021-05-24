"""
Order Application Views
=======================

"""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, request
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, )

from order.models import Order


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

    http_method_names = ["head", "options", "get"]
    model = Order

    def get(self, *args, **kwargs):
        order = self.get_object()
        if order.customer != self.request.user:
            redirect_url = reverse_lazy("order:list")
            return HttpResponseRedirect(redirect_url)

        return super(OrderDetailView, self).get(*args, **kwargs)


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Order card create view implementation"""

    model = Order
    fields = ["product", "quantity", "address"]

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
