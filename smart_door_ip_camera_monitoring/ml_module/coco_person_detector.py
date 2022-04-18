import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
import os

detector = None
def coco_person_init():
    module_handle = "https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2"

    handle = hub.load(module_handle)
    global detector
    detector = handle.signatures['serving_default']

def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    """Adds a bounding box to an image."""
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                    ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
                (left, top)],
                width=thickness,
                fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                    fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                display_str,
                fill="black",
                font=font)
        text_bottom -= text_height - 2 * margin

def draw_boxes(image, boxes, class_names, scores, max_boxes=100, min_score=0.1):
    """Overlay labeled boxes on an image with formatted scores and label names."""
    colors = list(ImageColor.colormap.values())
    font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score and class_names[i]==1:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
        display_str = "{}: {}%".format(class_names[i],
                                        int(100 * scores[i]))
        color = colors[hash(class_names[i]) % len(colors)]
        image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
        draw_bounding_box_on_image(
            image_pil,
            ymin,
            xmin,
            ymax,
            xmax,
            color,
            font,
            display_str_list=[display_str])
        np.copyto(image, np.array(image_pil))
    return image

def get_people_coco(image_np):
    # image_np = [np.expand_dims(image_np,axis=0)]
    # print(image_np.shape)
    converted_img  = tf.image.convert_image_dtype(image_np, tf.uint8)[tf.newaxis, ...]
    global detector
    if detector == None:
        coco_person_init()
    result = detector(converted_img)
    result = {key:value.numpy() for key,value in result.items()}

    scores = result['detection_scores'][0]
    d_class = result['detection_classes'][0]
    d_boxes = result['detection_boxes'][0]
    threshold = 0
    detected_person = [person for person in zip(scores, d_class, d_boxes) if person[0] > threshold and person[1] == 1]
    p_score, p_class ,p_box = zip(*detected_person)
    nms = tf.image.non_max_suppression(p_box, p_score, 20, score_threshold=.4, iou_threshold=.15)
    image_with_boxes = draw_boxes(
      image_np, np.array([p_box[i] for i in nms]),
      [p_class[i] for i in nms], [p_score[i] for i in nms])
    return nms.shape[0], image_with_boxes