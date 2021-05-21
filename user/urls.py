"""
User Application URLs Configuration
===================================

"""

from django.urls import path

from user.views import (user_logout, user_login, user_register)

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
    # path("profile/", UserProfileView.as_view(), name="profile"),
]