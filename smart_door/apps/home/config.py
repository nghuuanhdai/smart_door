# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'home'

    def ready(self):
        super().ready()
        from .ada_module import data_connect
        data_connect()
        from .ml_module.people_counter import ml_init
        ml_init()

        from .door_schedule_messenger import update_access_list
        update_access_list
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_access_list, 'interval', minutes=60)
        scheduler.start()