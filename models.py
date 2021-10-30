import json
import pickle
import random

import face_recognition
from datetime import datetime, timedelta
import subprocess
import settings
from voice_model import stream, recognizer


class Face(object):
    class_instances = []
    remember_seconds = settings.remember_seconds
    selected = None
    height_of_selected = 0

    def __init__(self, name: str, encoding):
        self.encoding = encoding
        self.name = name
        self._last_seen = datetime.now() - timedelta(seconds=Face.remember_seconds)
        self.class_instances.append(self)

    def see_you(self):
        self._last_seen = datetime.now()
        print('see:', self.name)

    def hello(self):
        Avatar.say(f'{random.choice(settings.PHRASES["hello"])}, {self.name}')

    @staticmethod
    def make_friends(encoding, name):
        # сохраняем кодировку в файл с именем лица
        face = Face(name, encoding)

        # переводим ndarray в формат для базы данных
        pickled_encoding = pickle.dumps(encoding)
        # Вставляем данные в таблицу
        settings.cursor.execute(f"INSERT INTO faces VALUES (?, ?)", (name, pickled_encoding))
        settings.conn.commit()

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


class Avatar:
    voice = 'Anna+CLB'

    def __init__(self):
        self.speech_rate = 90  # скорость речи
        self.speech_volume = 1  # громкость (0-1)

    @staticmethod
    def say(text):
        stream.stop_stream()
        shell = f'echo "{text}" | RHVoice-client -s {Avatar.voice} | aplay'
        print(f'--> {text}')
        process = subprocess.Popen(shell, shell=True)
        process.communicate()
        process.poll()
        stream.start_stream()

    @staticmethod
    def listen():
        text = None
        while not text:
            stream.start_stream()
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                return False

            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result())['text']
                stream.stop_stream()
                print(f'<-- {text}')
                return text

    @staticmethod
    def confirm(copy_that):
        if copy_that in random.choice(settings.PHRASES['positive'] + ['моё']):
            return True


