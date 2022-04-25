from datetime import datetime
import imp
from django.apps import AppConfig

class MyConfig(AppConfig):
    name = 'apps.home'
    label = 'home'

    def ready(self):
        super().ready()
        if not self.ready:
            return
        from .ada_module import data_connect
        data_connect()
        # from .ml_module.people_counter import ml_init
        # ml_init()
        from .models import Room
        rooms = Room.objects.all()
        for room in rooms:
            room.authorized_present = 0
            room.save()
        from .models import RoomPresent
        RoomPresent.objects.all().delete()
        
        from apscheduler.schedulers.background import BackgroundScheduler
        from .door_schedule_messenger import update_access_list
        update_access_list
        scheduler = BackgroundScheduler()
        scheduler.add_job(update_access_list, 'interval', minutes=60)
        scheduler.start()