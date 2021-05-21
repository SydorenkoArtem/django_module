"""
User Application Forms
======================
"""
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=32, help_text="32 characters or fewer")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(widget=forms.EmailInput)

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
            self.add_error("username", "username exists")
        except User.DoesNotExist:
            return username

    def clean(self):
        super(UserRegistrationForm, self).clean()
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            self.add_error("password1", "password does not match")
            self.add_error("password2", "password does not match")


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=32, help_text="32 characters or fewer")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    user = None

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            self.user = user
            return
        raise ValidationError("check username and password")
