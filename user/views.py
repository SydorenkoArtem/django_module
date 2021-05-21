from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from user.forms import UserRegistrationForm


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm

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
    else: # GET
        form = UserRegistrationForm()

    context = {
        "form": form
    }
    return render(request, "user/register.html", context)
