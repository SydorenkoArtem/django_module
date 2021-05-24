"""
Order Application Models
========================

"""

from django.db import models
from django.urls import reverse_lazy


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
    price = models.ForeignKey("product.Product", on_delete=models.SET_NULL, null=True)
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
