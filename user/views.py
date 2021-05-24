from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from user.forms import UserRegistrationForm, UserLoginForm


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data.get("username"),
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password1"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
            )
            redirect_url = reverse_lazy("login")
            return HttpResponseRedirect(redirect_url)
    else:
        form = UserRegistrationForm()

    context = {
        "form": form
    }
    return render(request, "user/register.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)
            redirect_url = reverse_lazy("list")
            return HttpResponseRedirect(redirect_url)
    else:
        form = UserLoginForm()

    return render(request, "user/login.html", {"form": form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    redirect_url = reverse_lazy("list")
    return HttpResponseRedirect(redirect_url)


class UserProfileView(LoginRequiredMixin, TemplateView):
    """"User profile view implementation"""

    template_name = "user/profile.html"