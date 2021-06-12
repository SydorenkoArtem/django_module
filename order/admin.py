"""
Order Application Admin
=======================

"""

from django.contrib import admin

from order.models import Order, OrderCart, OrderItem, Purchase


def get_product_quantity(order):
    return order.product.amount


def get_product_name(order):
    return str(order.product)


def get_prepare_order(order):
    return order.quantity < order.product.amount


def get_order_identifier(order):
    return f"{order.customer.username}-{order.oid}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order model admin implementation"""

    fields = ["status"]

    list_display = [
        "is_deleted",
        get_order_identifier,
        "created_at",
        "updated_at",
        get_product_name,
        get_product_quantity,
        "quantity",
        get_prepare_order,
        "status",
    ]
    list_editable = ["quantity", "status"]
    ordering = ["created_at", "updated_at"]


admin.site.register(OrderCart)
admin.site.register(OrderItem)
admin.site.register(Purchase)
