# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import ResetPassLink

# Register your models here.
@admin.register(ResetPassLink)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'link', 'expire_time']
