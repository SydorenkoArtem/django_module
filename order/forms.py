from django import forms
from django.core.exceptions import ValidationError

from order.models import Order
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
