from cProfile import Profile
import sys
from Adafruit_IO import MQTTClient
import json

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
    
def data_send_data(feed, data_dict):
    json_str = json.dumps(data_dict)
    print(f'sending {json_str} to {feed}')
    __shared_client.publish(feed, json_str)

def data_send_string(feed, string_data):
    print(f'sending {string_data} to {feed}')
    __shared_client.publish(feed, string_data)

if __name__ == "__main__":
    data_connect()
    while True:
        feed = input("Enter your feed: ")
        string_data = input("Enter string data: ")
        data_send_string(feed, string_data)
