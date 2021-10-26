import random
from models import Face, Avatar
import settings
import my_ear
import pickle


def examine_face(height, width, face_location):
    [(top, right, bottom, left)] = face_location
    frame_half_height, frame_half_width = height // 2, width // 2
    face_half_height, face_half_width = (bottom - top) // 2, (right - left) // 2
    face_center_y, face_center_x = top + face_half_height, left + face_half_width
    move_camera(frame_half_height - face_center_y, frame_half_width - face_center_x)

    if frame_half_height / 3 < face_half_height:
        # Если высота лица больше 1/3 кадра (достаточно близко)
        name = None
        # Давай познакомимся
        Avatar.say(random.choice(settings.PHRASES['make_friends']))

        while not name:
            name = my_ear.listen()

        for my_name_is in settings.PHRASES['my_name_is']:
            name = name.replace(my_name_is, '')
        return name

    else:
        Avatar.say(random.choice(settings.PHRASES['come_closer']))
        print('расстояние:', frame_half_height / 4 / face_half_height)


def read_face_encodings(path=settings.enc_path):

    for name, face_stored_pickled_data in settings.cursor.execute("SELECT name, encoding FROM faces"):
        encoding = pickle.loads(face_stored_pickled_data)
        Face(name, encoding)
        print(name, encoding)

    print(f'В памяти {len(Face.class_instances)} человек')


def move_camera(y, x):
    vertical, horizontal = 0, 0
    if y > 10:
        vertical = f'^ {y}'
    elif y < -10:
        vertical = f'v {y}'
    if x > 10:
        horizontal = f'{x} -->'
    elif x < -10:
        horizontal = f'<-- {x}'
    print('move', vertical, horizontal)
