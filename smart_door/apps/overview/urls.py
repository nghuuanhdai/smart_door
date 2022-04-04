# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import admin_overview

urlpatterns = [
    path('overview', admin_overview, name='overview'),
]
