import json
from channels.generic.websocket import WebsocketConsumer

class AdminControlConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        from .ada_module import register_onmessage
        register_onmessage(self)

    def on_mqtt_message(self, message):
        if 'LED' in message:
            self.send(text_data=json.dumps({
                'mqtt_message': True,
                'mqtt_data': message
            }))

    def disconnect(self, close_code):
        from .ada_module import deregister_onmessage
        deregister_onmessage(self)

    def receive(self, text_data):
        data_json = json.loads(text_data)
        if 'mqtt_message' in data_json:
            from .ada_module import ada_send_dict, AIO_DOORMONITOR
            print(data_json['mqtt_data'])
            ada_send_dict(AIO_DOORMONITOR, data_json['mqtt_data'])
        print(text_data)