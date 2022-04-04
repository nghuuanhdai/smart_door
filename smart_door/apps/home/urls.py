# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [
    path('check_schedule', views.check_schedule),
    path('rooms', views.rooms, name='rooms'),
    path('post/ajax/add_sched', views.add_sched, name='add_sched'),
    path('post/ajax/del_sched', views.del_sched, name='del_sched'),
    path('room_image_upload', views.room_image_upload, name='room_image_upload'),
    # The home page
    path('', views.index, name='home'),
    path('<slug:room>',views.room_detail, name='room_detail'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
