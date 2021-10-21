import os
import numpy as np
from faces import Face

enc_path = 'encodings'  # Файлы с кодом лиц


def read_face_encodings(path=enc_path):

    # Просмотреть все файлы кодов
    for enc_name in os.listdir(path):
        encoding_file = os.path.join(path, enc_name)
        encoding = np.loadtxt(encoding_file)
        Face(encoding, enc_name)

    return print('Known faces', len(Face.class_instances))


def write_face_encoding(name, encoding, path=enc_path):
    with open(os.path.join(path, name), "w") as f:
        for row in encoding:
            f.write(str(row))
            f.write('\n')


def move_camera(y, x):
    print('moving x', x, '; y', y)


def examine_face(height, width, face_location):
    [(top, right, bottom, left)] = face_location
    frame_half_height, frame_half_width = height // 2, width // 2
    face_half_height, face_half_width = (bottom - top) // 2, (right - left) // 2
    face_center_y, face_center_x = top + face_half_height, left + face_half_width
    if frame_half_height / 3 > face_half_height:
        print('Подойди ближе', frame_half_height / 3 / face_half_height)
    else:
        name = input('Как тебя зовут?')
        return name
    move_camera(frame_half_height - face_center_y, frame_half_width - face_center_x)
