import json
from threading import Thread
from time import sleep
import cv2
import numpy
from ml_module.coco_person_detector import get_people_coco
from ml_module.tf_lite_head_detector import get_people_tflite

MESSAGE_INTERVAL = 5 # unit seconds

def wait_for_exit():
    if cv2.waitKey(1) == ord("q"):
        return True
    return False

class VideoShow:
    def __init__(self, name):
        self.frame = None
        self.stopped = False
        self.name = name
        self.hasValidFrame = False

    def update(self, frame):
        self.frame = frame
        self.hasValidFrame = True

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            if self.hasValidFrame:
                cv2.imshow(self.name,  self.frame)
            if wait_for_exit():
                self.stopped = True
    def stop(self):
        self.stopped = True

class VideoDetection(VideoShow):
    def __init__(self, name):
        super().__init__(name)
        self.count = 0
        self.raw_frame = None
        self.raw_frame_available = False

    def update(self, frame):
        self.raw_frame = frame
        self.raw_frame_available = True

    def show(self):
        while not self.stopped:
            if self.raw_frame_available:
                self.count, self.frame = get_people_tflite(numpy.asarray(self.raw_frame))
                self.hasValidFrame = True
            if self.hasValidFrame:
                cv2.imshow(self.name,  self.frame)
            if wait_for_exit():
                self.stopped = True


def ipCameraMonitor(ip_camera_config, result):
    cap = cv2.VideoCapture(ip_camera_config["url"])
    print(f'start monitoring {ip_camera_config["url"]}')
    raw_video_shower = VideoShow(ip_camera_config["room_id"]+"_raw").start()
    analysed_shower = VideoDetection(ip_camera_config["room_id"]+"_detection").start()

    while True:
        grapped, frame = cap.read()
        raw_video_shower.update(frame)
        analysed_shower.update(frame)
        result.count = analysed_shower.count
        if wait_for_exit():
            break

import os
dirname = os.path.dirname(__file__)
config_path = os.path.join(dirname, 'ip_camera_conf.json')
with open(config_path) as config_file:
    configs = json.load(config_file)

class RoomDetectionResult:
    def __init__(self, roomId, camImgUrl):
        self.roomId = roomId
        self.count = 0
        self.camImgUrl = camImgUrl

    def __repr__(self):
        return f"{{room: {self.roomId}, count: {self.count}}}\n"

def detection_thread(callback):
    detection_results = []
    index = 0
    for config in configs:
        roomResult = RoomDetectionResult(config["room_id"], config["room_image_url"])
        detection_results.append(roomResult)
        Thread(target=ipCameraMonitor, args=[config, roomResult]).start()
        index+=1

    while True:
        callback(detection_results)
        sleep(MESSAGE_INTERVAL)

def start_detection(callback):
    Thread(target=detection_thread, args=[callback]).start()

##########################
##
## Install IP camera on an android device and update ip_camera_conf.json
## Call start_detection(callback) on gateway server with the callback to send the data to mqtt server
##
##
##########################

def detection_result(results):
    print(results)

if __name__ == "__main__":
    start_detection(detection_result)