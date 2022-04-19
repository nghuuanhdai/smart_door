from ml_module.people_counter import get_people_in_room_from_image
import os

get_people_in_room_from_image(os.path.join(os.path.dirname(__file__),'test.jpg'))