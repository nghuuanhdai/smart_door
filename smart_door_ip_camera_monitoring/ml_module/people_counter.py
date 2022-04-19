from operator import imod
import numpy as np
from PIL import Image
import os
from .tf_lite_head_detector import init_tflite, get_people_tflite
from .coco_person_detector import coco_person_init, get_people_coco

def ml_init():
  init_tflite()
  coco_person_init()

# def get_people_in_room_from_image(image_path):
#   img2 = cv2.imread(file)

#   img = tf.io.read_file(image_path)
#   img = tf.image.decode_jpeg(img, channels=3)
#   coco_count, coco_image = get_people_coco(image_path)
#   tflite_count, tf_image = get_people_tflite(image_path)
#   return coco_count, tflite_count, coco_image, tf_image

def get_people_in_room_from_image(cvFrame):
  coco_count, coco_image = get_people_coco(cvFrame)
  tflite_count, tf_image = get_people_tflite(cvFrame)
  return coco_count, tflite_count, coco_image, tf_image