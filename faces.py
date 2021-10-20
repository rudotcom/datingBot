import datetime
import os

import face_recognition
import numpy as np

faces = []

enc_path = 'encodings'  # known people encodings to be saved to


class Face(object):

    def __init__(self, encoding, name: str):
        self.encoding = encoding
        self.name = name
        self.last_seen = datetime.datetime.now()

    def see_you(self):
        self.last_seen = datetime.datetime.now()

    def apply_nearest_encoding(self, encoding_batch: list, name: str):
        # выбрать значение с минимальным средним расстоянием до всех остальных

        row_array = []
        for row in range(0, len(encoding_batch)):
            # проходим список
            cells_array = []
            for cell in range(0, len(encoding_batch)):
                # проходим ячейки, индекс которых больше индекса ряда
                # (чтобы не сравнивать с собой дважды с другими)
                # находим расстояния между значением ряда и значениями ячеек
                distance = face_recognition.face_distance(
                    encoding_batch[row], encoding_batch[cell]
                )
                cells_array.append(distance)

            # находим среднее в ряду
            average = np.mean(cells_array)
            # print('average', encoding_batch[row], average)
            # собираем ряд из средних значений
            row_array.append(average)

        best_match_index = np.argmin(row_array)
        self.encoding = encoding_batch[best_match_index]

        # сохраняем кодировку в файл с именем лица
        with open(os.path.join(enc_path, name), "w") as f:
            for row in self.encoding:
                f.write(str(row))
                f.write('\n')


def read_face_encodings():
    for enc_dir in os.listdir(enc_path):

        known_name = os.path.basename(enc_dir)
        encoding_file = os.path.join(enc_path, known_name)

        if os.path.isfile(encoding_file):
            face_encoding = np.loadtxt(encoding_file)
            face = Face(face_encoding, known_name)
            faces.append(face)


def find_name(encoding):
    for face in faces:
        face_distance = face_recognition.face_distance(face.encoding, encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            return face.name
