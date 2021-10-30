import random

import face_recognition
import numpy as np

from models import Face, Avatar
import settings
import pickle
from math import sqrt


def distance_to_center(height, width, face_location):
    print('location:', face_location)
    [(top, right, bottom, left)] = face_location
    frame_half_height, frame_half_width = height // 2, width // 2
    face_half_height, face_half_width = (bottom - top) // 2, (right - left) // 2
    # расстояние от центра лица до центра кадра
    return sqrt((top + face_half_height - frame_half_height) ** 2 + (left + face_half_width - frame_half_width) ** 2)


def take_a_close_look(face_encodings, selected_face_encoding):
    # выбрать из присутствующих на текущем кадре лиц то же лицо из предыдущего кадра
    matches = face_recognition.compare_faces(face_encodings, selected_face_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        return face_encodings[first_match_index]

    for face_encoding in face_encodings:
        # Посмотреть, есть ли похожие среди присутствующих (ближайшее к нему)
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return face_encodings[best_match_index]


def move_selected_face_to_center(height, width, face_location):
    print('location:', face_location)
    [(top, right, bottom, left)] = face_location
    frame_half_height, frame_half_width = height // 2, width // 2
    face_half_height = (bottom - top) // 2
    face_center_y = top + face_half_height
    face_center_x = left + (right - left) // 2
    move_camera(frame_half_height - face_center_y, frame_half_width - face_center_x)
    return frame_half_height, face_half_height


def is_face_close(frame_half_height, face_half_height):
    # Если высота лица больше 1/3 высоты кадра (лицо достаточно близко)
    if frame_half_height / 3 < face_half_height:
        Avatar.say(random.choice(settings.PHRASES['come_closer']))
        print('расстояние:', frame_half_height / 4 / face_half_height)


def ask_name():
    # Давай познакомимся
    Avatar.say(random.choice(settings.PHRASES['make_friends']))

    name = Avatar.listen()

    for my_name_is in settings.PHRASES['my_name_is']:
        name = name.replace(my_name_is, '')

    # тебя зовут ..., правильно?
    Avatar.say(random.choice(settings.PHRASES['your_name_is']))
    Avatar.say(name)
    Avatar.say(random.choice(settings.PHRASES['is_your_name']))
    # если ответ положительный
    if Avatar.confirm(Avatar.listen()):
        return name


def read_face_encodings():

    for name, face_stored_pickled_data in settings.cursor.execute("SELECT name, encoding FROM faces"):
        encoding = pickle.loads(face_stored_pickled_data)
        Face(name, encoding)

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
