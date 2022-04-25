# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from csv import list_dialects
import imp
from django.contrib import admin
from .models import Profile, Room, Schedule, RoomAccessLog, RoomPresent

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_id']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'contactInfo', 'current_people_count', 'max_occupancy', 'authorized_present']

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'time_slot', 'schedule_date']

@admin.register(RoomAccessLog)
class RoomAccessLogAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'temp', 'status']


@admin.register(RoomPresent)
class RoomPresentAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'temp']