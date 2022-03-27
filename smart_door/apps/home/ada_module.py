from cProfile import Profile
import sys
from Adafruit_IO import MQTTClient
import json

from .models import Room, RoomAccessLog, RoomPresent

AIO_USERNAME = "khanhhungvu1508"
AIO_KEY = "aio_pcJU685m50e7ScdBM6EbAhS28hze"
AIO_DOORMONITOR = "MSG_DOOR2_DoorMonitor"
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



def data_send_data(feed, data):
    json_str = json.dumps(data.__dict__)
    print(f'sending {json_str} to {feed}')
    __shared_client.publish(feed, json_str)