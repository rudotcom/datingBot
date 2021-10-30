import cv2
import face_recognition

from utils import read_face_encodings, take_a_close_look, distance_to_center, move_selected_face_to_center, \
    is_face_close, ask_name
from models import Face
from settings import image_source

if __name__ == '__main__':
    read_face_encodings()

    frame_count = 0
    process_every_frame = 20

    # # Получить поток с IP камеры
    video_capture = cv2.VideoCapture(image_source)

    while video_capture.isOpened():
        selected_face_encoding = None
        person = None
        # Захват единичного кадра видео
        ret, frame = video_capture.read()

        if ret:

            # Пропускаем по несколько кадров для ускорения процесса
            if frame_count % process_every_frame == 0:
                face_distances = []

                # Конвертация изображения из цветов BGR (которые испоользует OpenCV)
                # в цвета RGB (которые использует face_recognition)
                rgb_frame = frame[:, :, ::-1]

                # Найти все лица и их кодировки в текущем кадре видео
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                height, width = frame.shape[:2]

                for face in range(len(face_locations)):
                    # если есть кандидат в знакомые, найти на текущем кадре
                    if selected_face_encoding:
                        selected_face_encoding = take_a_close_look(face_encodings, selected_face_encoding)
                        selected_face_location = face_locations[face]
                        frame_half_height, face_half_height = move_selected_face_to_center(
                            height, width, selected_face_location)

                        is_face_close(frame_half_height, face_half_height)

                    # для каждого номера лица определяем знакомо ли лицо
                    person = Face.by_encoding(face_encodings[face])

                    # Если знакомо
                    if person:
                        # если давно не виделись
                        if not person.recently_seen:
                            # Поприветствовать лицо
                            person.hello()
                        # обозначить, что увиделись
                        person.see_you()

                    # если есть незнакомые лица
                    else:
                        # если лицо не выбрано из незнакомых
                        if not selected_face_encoding:
                            height, width = frame.shape[:2]
                            # узнать расстояние лица до центра
                            distance = distance_to_center(height, width, face_locations[face])
                            # добавляем в список незнакомых лиц с параметром [0] = расстояние
                            face_distances.append((distance, face_locations[face], face_encodings[face]))

                        else:  # если неизвестное лицо таки найдено
                            name = ask_name()
                            if name:
                                Face.make_friends(selected_face_encoding, name)

                if face_distances:
                    # выбираем лицо с минимальным расстоянием до центра
                    # Запомнить encoding ближайшего кандидата
                    selected_face_encoding = min(face_distances, key=lambda x: x[0])[2]

                print(frame_count)

            frame_count += 1

