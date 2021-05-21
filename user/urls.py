"""
User Application URLs Configuration
===================================

"""

from django.urls import path

from user.views import (UserRegistrationForm)

urlpatterns = [
    # path("login/", UserLoginForm, name="login"),
    # path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegistrationForm, name="register"),
    # path("profile/", UserProfileView.as_view(), name="profile"),
]