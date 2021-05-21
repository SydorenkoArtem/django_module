"""
Product Application Forms
=========================

"""

from django import forms

from product.models import Review


class ReviewForm(forms.ModelForm):
    """Review form implementation"""

    class Meta:
        model = Review
        fields = ["rate", "review"]
        widgets = {
            "rate": forms.Select(attrs={"class": "form-select"}),
            "review": forms.TextInput(attrs={"class": "form-control"})
        }
