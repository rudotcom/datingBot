import os
import random

import numpy as np
from models import Face, Avatar
import settings
import my_ear


def read_face_encodings(path=settings.enc_path):

    # Просмотреть все файлы кодов
    for enc_name in os.listdir(path):
        encoding_file = os.path.join(path, enc_name)
        encoding = np.loadtxt(encoding_file)
        Face(encoding, enc_name)

    return print(f'Я знаю {len(Face.class_instances)} человек')


def write_face_encoding(name, encoding, path=settings.enc_path):
    with open(os.path.join(path, name), "w") as f:
        for row in encoding:
            f.write(str(row))
            f.write('\n')


def move_camera(y, x):
    vertical, horizontal = 0, 0
    if y > 10:
        vertical = f'^ {y}'
    elif y < -10:
        vertical = f'v {y}'
    if x > 10:
        horizontal = f'--> {x}'
    elif x < -10:
        horizontal = f'<-- {x}'
    print('move', vertical, horizontal)


def examine_face(height, width, face_location):
    [(top, right, bottom, left)] = face_location
    frame_half_height, frame_half_width = height // 2, width // 2
    face_half_height, face_half_width = (bottom - top) // 2, (right - left) // 2
    face_center_y, face_center_x = top + face_half_height, left + face_half_width
    if frame_half_height / 3 > face_half_height:
        Avatar.say('Подойди ближе')
        print(frame_half_height / 4 / face_half_height)
    else:
        Avatar.say(random.choice(settings.PHRASES['make_friends']))
        name = my_ear.listen()
        return name
    move_camera(frame_half_height - face_center_y, frame_half_width - face_center_x)
