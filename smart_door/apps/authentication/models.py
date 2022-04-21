# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResetPassLink(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    link = models.TextField(max_length=32)
    expire_time = models.DateTimeField()