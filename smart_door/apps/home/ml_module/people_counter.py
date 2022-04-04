import numpy as np
from PIL import Image
import os
from .tf_lite_head_detector import *

detector = None

def ml_init():
  # Load the TFLite model
  options = ObjectDetectorOptions(
    num_threads=4,
    score_threshold=0.2,
  )
  global detector
  detector = ObjectDetector(model_path=os.path.join(os.path.dirname(__file__), 'head.tflite'), options=options)

def get_people_in_room_from_image(image_path):
  image = Image.open(image_path).convert('RGB')
  image.thumbnail((512, 512), Image.ANTIALIAS)
  image_np = np.asarray(image)
  global detector
  if detector == None:
    ml_init()
  detections = detector.detect(image_np)
  image_np = visualize(image_np, detections)
  Image.fromarray(image_np).save(image_path)
  return len(detections)