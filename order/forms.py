from django import forms
from django.core.exceptions import ValidationError

from order.models import Order, Purchase, OrderItem
from product.models import Product
from user.models import Cash


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].empty_label = "Not selected Product"

    class Meta:
        model = Order
        fields = ["product", "quantity", "address"]

    def clean(self):
        super(OrderForm, self).clean()
        quantity = self.cleaned_data.get("quantity")
        product = self.cleaned_data.get("product")
        amount_product = Product.objects.get(product=product).amount
        # user = {request.user.username}
        # cash = Cash.objects.get(username=user).amount
        if quantity > amount_product:
            raise ValidationError(f"This quantity is not in stock {amount_product}")
        # if Order.total_price > 3000:
        #     raise ValidationError(f"Not enough money. In your account 3000")


class CartEntityForm(forms.ModelForm):
    """Cart entity form implementation"""

    quantity = forms.IntegerField(
        min_value=1,
    )

    class Meta:
        model = OrderItem
        fields = ["id", "quantity"]

        widgets = {
            "quantity": forms.NumberInput(attrs={
                "class": "col-1 numberinput form-control"
            })
        }


CartEntitiesFormSet = forms.modelformset_factory(
    OrderItem, form=CartEntityForm, extra=0
)


class PurchaseForm(forms.ModelForm):
    """Purchase form implementation"""

    address = forms.CharField(
        label=("address"),
        max_length=128,
    )
    city = forms.CharField(
        label=("city name"),
        max_length=128,
    )
    zipcode = forms.CharField(
        label=("zip code"),
        max_length=6,
    )
    country = forms.CharField(
        label=("country"),
        max_length=32,
    )

    class Meta:
        model = Purchase
        fields = [
            "address",
            "city",
            "zipcode",
            "country",
        ]

    def get_shipping_address(self):
        super(PurchaseForm, self).clean()
        address = self.cleaned_data.get("address")
        city = self.cleaned_data.get("city")
        zipcode = self.cleaned_data.get("zipcode")
        country = self.cleaned_data.get("country")

        return f"{address}, {city}, {zipcode}, {country}"

    def save(self, commit=True):
        self.instance.shipping_address = self.get_shipping_address()
        super(PurchaseForm, self).save()
