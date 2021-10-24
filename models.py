import os
import face_recognition
from datetime import datetime, timedelta

import settings
faces = []


class Face(object):
    class_instances = []
    remember_seconds = settings.remember_seconds

    def __init__(self, encoding, name: str):
        self.encoding = encoding
        self.name = name
        self._last_seen = datetime.now() - timedelta(seconds=Face.remember_seconds)
        self.class_instances.append(self)

    def see_you(self):
        self._last_seen = datetime.now()
        print('see:', self.name)

    def hello(self):
        Avatar.say(f'Здравствуй, {self.name}')

    @staticmethod
    def make_friends(encoding, name):
        face = Face(encoding, name)
        # сохраняем кодировку в файл с именем лица
        with open(os.path.join(settings.enc_path, name), "w") as f:
            for row in encoding:
                f.write(str(row))
                f.write('\n')
        Avatar.say(f'Приятно познакомиться, {name}')
        face.see_you()

    @property
    def recently_seen(self):
        # True если было видимо меньше чем remember_seconds назад
        return (datetime.now() - self._last_seen).seconds < Face.remember_seconds

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


class Avatar(object):
    listening = True
    voice = 'anna'

    def __init__(self):
        self.speech_rate = 130  # скорость речи 140 самый норм
        self.speech_volume = 1  # громкость (0-1)

    @classmethod
    def say(cls, text):
        cls.listening = False
        s = f'echo "{text}" | RHVoice-test -p {cls.voice}'
        os.system(s)
        cls.listening = True
