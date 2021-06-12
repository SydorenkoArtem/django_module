"""
Order Application Models
========================

"""

from django.db import models
from django.urls import reverse_lazy

from product.models import Product


class Order(models.Model):
    class Meta:
        db_table = "order"
        verbose_name = "order"
        verbose_name_plural = "orders"

    oid = models.BigAutoField(primary_key=True)

    CREATED = 1
    CANCELED = 2
    CONFIRMED = 3
    COMPLETED = 4
    REJECTED = 5

    ORDER_STATUSES = [
        [CREATED, "Created"],
        [CANCELED, "Canceled"],
        [CONFIRMED, "Confirmed"],
        [COMPLETED, "Completed"],
        [REJECTED, "Rejected"],
    ]

    status = models.IntegerField(choices=ORDER_STATUSES, default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField(null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_deleted = models.BooleanField(default=False)
    customer = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="+",
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
    )

    def __repr__(self):
        """Return a string representation of an instance"""

        return f"<Order ({self.id})>"

    def __str__(self):
        """Return a string version of an instance"""

        return f"{self.product} ({self.quantity})"

    def get_absolute_url(self):
        """Return an absolute URLs for an instance"""

        return reverse_lazy("order:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        price = Product.objects.get(product=self.product).price
        self.total_price = self.quantity * price
        super(Order, self).save(*args, **kwargs)


class OrderCart(models.Model):
    customer = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="+",
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderCart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Purchase(models.Model):
    """Purchase model implementation"""

    class Meta:
        db_table = "purchase"
        verbose_name = ("purchase")
        verbose_name_plural = ("purchases")

    cart = models.OneToOneField(
        OrderCart,
        on_delete=models.CASCADE,
        related_name="purchase",
        verbose_name=("shopping cart"),
    )

    purchased_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=("purchased datetime"),
    )

    shipping_address = models.TextField()

    def __repr__(self):
        """Return a string representation of an instance"""

        return f"<Purchase ({self})>"

    def __str__(self):
        """Return a string version of an instance"""

        return f"{self.purchased_at}"

    @property
    def customer(self):
        """Return a customer instance"""

        return self.cart.customer

    def get_absolute_url(self):
        return reverse_lazy("purchase:detail", kwargs={"pk": self.pk})

    def get_total(self):
        """Return a total price of an instance"""

        return self.cart.get_cart_total()

    def save(self, *args, **kwargs):
        self.cart.complete = True
        self.cart.save()

        self.cart.customer.cash.amount -= self.get_total()
        self.cart.customer.cash.save()

        super(Purchase, self).save(*args, **kwargs)
