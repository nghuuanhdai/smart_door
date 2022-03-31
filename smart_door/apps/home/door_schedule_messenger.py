from datetime import date, datetime
class RoomAccessData:
    ROOM = '0'
    SCHEDULE_BEGIN = []

def update_access_list():
    from .models import Room, Schedule
    from .ada_module import data_send_data, AIO_DOORMONITOR

    crr_date = datetime.today().date()
    crr_hour = datetime.now().hour
    rooms = Room.objects.all()
    for room in rooms:
        schedules = Schedule.objects.filter(room=room).filter(schedule_date=crr_date).filter(time_slot=crr_hour)
        access_ids = [schedule.user.profile.card_id for schedule in schedules]
        access_data = RoomAccessData()
        access_data.ROOM = room.id
        access_data.SCHEDULE_BEGIN = access_ids

        data_send_data(AIO_DOORMONITOR, access_data)