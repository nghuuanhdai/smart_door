# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class RoomAccessData:
    ROOM = '0'
    SCHEDULE_BEGIN = []

class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'home'

    def ready(self):
        super().ready()
        from .ada_module import data_connect
        data_connect()
        from .ml_module.people_counter import ml_init
        ml_init()

        self.update_access_list()
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.update_access_list, 'interval', minutes=60)
        scheduler.start()

    

    def update_access_list(self):
        from .models import Room, Schedule
        from .ada_module import data_send_data, AIO_DOORMONITOR

        crr_date = datetime.today()
        crr_hour = datetime.now().hour
        rooms = Room.objects.all()
        for room in rooms:
            schedules = Schedule.objects.filter(room=room).filter(schedule_date=crr_date).filter(time_slot=crr_hour)
            access_ids = [schedule.user.profile.card_id for schedule in schedules]
            access_data = RoomAccessData()
            access_data.ROOM = room.id
            access_data.SCHEDULE_BEGIN = access_ids

            data_send_data(AIO_DOORMONITOR, access_data)

