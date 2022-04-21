# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, forget_pass, reset_pass
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('forget_pass/', forget_pass, name="forget_pass"),
    path('reset_pass/<slug:link>', reset_pass, name="reset_pass"),
    path("logout/", LogoutView.as_view(), name="logout")
]
