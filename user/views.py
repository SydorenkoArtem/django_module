from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from user.forms import UserSignUpForm


class UserProfileView(LoginRequiredMixin, TemplateView):
    """"User profile view implementation"""

    template_name = "user/profile.html"


class UserSignUpView(CreateView):
    """User sign-up view implementation"""

    form_class = UserSignUpForm
    template_name = "user/register.html"
    success_url = reverse_lazy("user:login")


class UserSignInView(LoginView):
    """User sign-in view implementation"""

    template_name = "user/login.html"
    success_url = reverse_lazy("list")


class UserLogoutView(LogoutView):
    """User logout view implementation"""

    success_url = reverse_lazy("list")

