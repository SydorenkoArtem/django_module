"""
Product Application Forms
=========================

"""

from django import forms

from product.models import Product


class ProductForm(forms.ModelForm):
    """Review form implementation"""

    class Meta:
        model = Product
        fields = ["amount"]
        widgets = {
            "amount": forms.Select(attrs={"class": "form-select"}),
            # "review": forms.TextInput(attrs={"class": "form-control"})
        }
