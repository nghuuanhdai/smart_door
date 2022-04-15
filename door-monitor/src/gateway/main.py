import serial
from time import sleep
import sys
from Adafruit_IO import MQTTClient
import json

AIO_USERNAME = "khanhhungvu1508"
AIO_KEY = "aio_pcJU685m50e7ScdBM6EbAhS28hze"
AIO_DOORMONITOR = ["LED_DoorMonitor", "DOOR_DoorMonitor", "NUMPEOPLE_DoorMonitor", "MSG_DoorMonitor"]

arduino = serial.Serial(port='COM2', baudrate=9600, timeout=.1)

room_id = "1"

def  connected(client):
    print("Connected...")
    for feed in AIO_DOORMONITOR:
        client.subscribe(feed)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully...")

def  disconnected(client):
    print("Disconnected...")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Topics: " + feed_id)
    print("Received data: " + payload)
    if (feed_id == "LED_DoorMonitor" and payload == "1"):
        arduino.write(bytes("#ROOM " + room_id + " LED_ON*", 'UTF-8')) # Suppose we only consider ROOM 0
    elif (feed_id == "LED_DoorMonitor" and payload == "0"):
        arduino.write(bytes("#ROOM " + room_id + " LED_OFF*", 'UTF-8')) # Suppose we only consider ROOM 0
    elif (feed_id == "DOOR_DoorMonitor" and payload == "1"):
        arduino.write(bytes("#ROOM " + room_id + " DOOR_OPEN*", 'UTF-8')) # Suppose we only consider ROOM 0
    elif (feed_id == "MSG_DoorMonitor"):
        jsonobj = json.loads(payload)
        # Always have syntax of json
        # {
        #   "ROOM": xxx,
        #   "xxx": xxx
        # }
        if (list(jsonobj.keys())[1] == "SCHEDULE_BEGIN"):
            msg = "#ROOM " + jsonobj["ROOM"] + " SCHEDULE_BEGIN"
            for id_people in jsonobj["SCHEDULE_BEGIN"]:
                msg = msg + " " + id_people
            msg += "*"
            arduino.write(bytes(msg, 'UTF-8'))
        elif (list(jsonobj.keys())[1] == "USERID_SCAN"):
            msg = "#ROOM " + jsonobj["ROOM"] + " USERID_SCAN " + jsonobj["USERID_SCAN"] + "*"
            arduino.write(bytes(msg, 'UTF-8'))

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def data_processing(data):
    if data.endswith("#\\r\\n") & data.startswith("*"):
        data = data.replace ("#\\r\\n", "")
        data = data.replace ("*", "")
        return data.split()
        

def send_data(data):
    if(len(data)):
        data = data.replace ("b'", "")
        data = data.replace ("'", "")
        d = data_processing(data)
        if (d != None):
            if (d[2] == "LED"):
                if (d[1] == '0'):
                    msg = '{"ROOM": "' + d[1] + '", "LED": "' + d[3] + '"}'
                    client.publish(AIO_DOORMONITOR[0], d[3])
                    client.publish(AIO_DOORMONITOR[3], msg)
            # elif (d[0] == "DOOR"):
            #     client.publish(AIO_DOORMONITOR[1], d[1])
            elif (d[2] == "NUMPEOPLE"):
                if (d[1] == "0"): # Suppose we only consider ROOM0 and want to publish it
                    msg = '{"ROOM": "' + d[1] + '", "NUMPEOPLE": "' + d[3] + '"}'
                    client.publish(AIO_DOORMONITOR[2], d[3])
                    client.publish(AIO_DOORMONITOR[3], msg)
            elif (d[2] == "ID"):
                if (d[1] == "0"): # Suppose we only consider ROOM0 and want to publish it
                    msg = ""
                    if (len(d) == 8): #Have format ROOM xxx ID xxx TEMPERATURE xxx STATUS xxx
                        msg = '{"ROOM": "' + d[1] + '", "ID": "' + d[3] + '", "TEMPERATURE": "' + d[5] + '", "STATUS": "' + d[7] + '"}'
                    else: #Have format ROOM xxx ID xxx STATUS xxx
                        msg = '{"ROOM": "' + d[1] + '", "ID": "' + d[3] + '", "STATUS": "' + d[5] + '"}'
                    client.publish(AIO_DOORMONITOR[3], msg)   

dump_temperature = 30
dump_humidity = 20

while True:
    if(arduino.in_waiting):
        data = str(arduino.readline())
        print(data)
        send_data(data)
    sleep(1)
    pass