# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('room_image_upload', views.room_image_upload),
    path('check_schedule', views.check_schedule),
    path('rooms', views.rooms, name='rooms'),
    path('room/<slug:room>',views.room_detail, name='room_detail'),
    # The home page
    path('', views.index, name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
