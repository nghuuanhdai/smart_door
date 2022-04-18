from cProfile import Profile
import sys
from Adafruit_IO import MQTTClient
import json

from .models import Room, RoomAccessLog, RoomPresent
from .mail_module import alert_admin
from datetime import date, datetime
import requests
import shutil
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

AIO_USERNAME = "khanhhungvu1508"
AIO_KEY = "aio_pcJU685m50e7ScdBM6EbAhS28hze"
AIO_DOORMONITOR = "MSG_DoorMonitor"
AIO_FEEDS = [AIO_DOORMONITOR]

__shared_client = None
def data_connect():
    global __shared_client
    __shared_client = MQTTClient(AIO_USERNAME , AIO_KEY)
    __shared_client.on_connect = connected
    __shared_client.on_disconnect = disconnected
    __shared_client.on_message = message
    __shared_client.on_subscribe = subscribe
    __shared_client.connect()
    __shared_client.loop_background()

def connected(client):
    print("Connected...")
    for feed in AIO_FEEDS:
        __shared_client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully...")

def disconnected(client):
    print("Disconnected...")

def message(client , feed_id , payload):
    print(f'receive {feed_id}: \n{[payload]}\n')
    data = json.loads(payload)
    if "Status" in data:
        status = data["Status"]
        if status == "ALLOW":
            card_id = data["ID"]
            room_id = data["ROOM"]
            
            room = Room.objects.get(id=int(room_id))
            user = Profile.objects.get(card_id=card_id).user

            temp = data["Temperature"]
            access_log = RoomAccessLog()
            access_log.user = user
            access_log.room = room
            access_log.temp = temp
            access_log.status = RoomAccessLog.STATUS_ALLOWED

            access_log.save()
            
            room_present = RoomPresent()
            room_present.user = user
            room_present.room = room
            room_present.temp = temp
            room_present.save()

            room.authorized_present += 1
            room.save()

        if status == "NOT_ALLOW":
            card_id = data["ID"]
            room_id = data["ROOM"]
            room = Room.objects.get(id=int(room_id))
            user = Profile.objects.get(card_id=card_id).user

            temp = data["Temperature"]
            access_log = RoomAccessLog()
            access_log.user = user
            access_log.room = room
            
            access_log.temp = temp
            access_log.status = RoomAccessLog.STATUS_DENIED

            access_log.save()

        if status == "OUT_ROOM":
            card_id = data["ID"]
            room_id = data["ROOM"]

            room = Room.objects.get(id=int(room_id))
            user = Profile.objects.get(card_id=card_id).user
            access_log = RoomAccessLog()
            access_log.user = user
            access_log.room = room
            access_log.status = RoomAccessLog.STATUS_DENIED

            access_log.save()
            
            room_present = RoomPresent.objects.get(user=user, room=room)
            room_present.delete()

            room.authorized_present -= 1
            room.save()
    
    if "HEAD_COUNT" in data:
        room_id = data["ROOM"]
        head_count = data["HEAD_COUNT"]
        image_url = data["IMAGE_URL"]

        print(head_count)
        try:
            room = Room.objects.get(id=room_id)
            present_number = RoomPresent.objects.filter(room=room).count()
            
            if head_count > room.current_people_count and head_count > present_number:
                r = requests.get(url=image_url)
                image_paths = {}
                if r.status_code == 200:
                    path = os.path.join(BASE_DIR, "static/upload/", str(room_id)+'.jpg')
                    with open(path, 'wb') as f:
                        f.write(r.content)
                    image_paths = {f'room{room_id}_[{datetime.now()}]': path}
                send_over_crowded_warning(room_id, head_count, present_number, image_paths)
            
            room.current_people_count = head_count
            room.save()

        except Room.DoesNotExist:
            pass

def send_over_crowded_warning(room_id, people_in_image, people_in_schedule, image_paths):
    try:
        print("alert admin")
        room = Room.objects.get(id=room_id)
        alert_email = room.room_alert_email
        alert_admin(alert_email, f'Unexpected number of people in room {room.name}', f'{datetime.now()}\nexpect this room to have {people_in_schedule}, but detected {people_in_image}', image_paths)
    except Room.DoesNotExist:
        return

def data_send_data(feed, data):
    json_str = json.dumps(data.__dict__)
    print(f'sending {json_str} to {feed}')
    __shared_client.publish(feed, json_str)