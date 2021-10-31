import cv2
import face_recognition
import numpy as np
from PIL import Image

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
        person = None
        # Захват единичного кадра видео
        ret, frame = video_capture.read()
        # img_pil = Image.fromarray(frame)

        if ret:  # True = кадр доступен

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
                    if Face.selected is not None:
                        Face.selected = take_a_close_look(face_encodings, Face.selected)
                        selected_face_location = tuple(face_locations[face])
                        print(selected_face_location)
                        frame_half_height, face_half_height = move_selected_face_to_center(
                            height, width, selected_face_location)

                        if is_face_close(frame_half_height, face_half_height):
                            # если лицо кандидата достаточно близко
                            name = ask_name()
                            if name:
                                Face.make_friends(Face.selected, name)

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
                        if Face.selected is not False:
                            height, width = frame.shape[:2]
                            # узнать расстояние лица до центра
                            distance = distance_to_center(height, width, face_locations[face])
                            # добавляем в список незнакомых лиц с параметром [0] = расстояние
                            face_distances.append((distance, face_locations[face], face_encodings[face]))

                if face_distances:
                    print('неизвестных', len(face_distances))
                    # выбираем лицо с минимальным расстоянием до центра
                    # Запомнить encoding ближайшего кандидата
                    Face.selected = min(face_distances, key=lambda x: x[0])[2]

                print(frame_count)
                # frame = np.array(img_pil)

            frame_count += 1
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cv2.imshow('What I see', frame)

# Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
