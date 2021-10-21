from datetime import datetime, timedelta
import os

import face_recognition
import numpy as np

faces = []

enc_path = 'encodings'  # known people encodings to be saved to


class Face(object):
    class_instances = []
    remember_seconds = 7200

    def __init__(self, encoding, name: str):
        self.encoding = encoding
        self.name = name
        self._last_seen = datetime.now() - timedelta(seconds=Face.remember_seconds)
        self.class_instances.append(self)

    def see_you(self):
        self._last_seen = datetime.now()

    @property
    def recently_seen(self):
        # True если было видимо меньше чем remember_seconds назад
        return (datetime.now() - self._last_seen).seconds < Face.remember_seconds

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

    @classmethod
    def by_encoding(cls, encoding):
        minimal_distance = 1
        for person in cls.class_instances:
            # if face_recognition.compare_faces([person.encoding], encoding):
            #     return person

            # Если совпадение не найдено, смотрим похоже ли лицо на лицо из класса
            face_distance = face_recognition.face_distance([person.encoding], encoding)

            if face_distance < minimal_distance:
                minimal_distance = face_distance
                closest_face = person

        if minimal_distance < 0.60:
            return closest_face

