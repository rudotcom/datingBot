import cv2
import face_recognition

from utils import read_face_encodings, examine_face
from models import Avatar, Face
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

        if ret:

            # Пропускаем по несколько кадров для ускорения процесса
            if frame_count % process_every_frame == 0 and Avatar.listening:

                # Конвертация изображения из цветов BGR (которые испоользует OpenCV)
                # в цвета RGB (которые использует face_recognition)
                rgb_frame = frame[:, :, ::-1]

                # Найти все лица и их кодировки в текущем кадре видео
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding in face_encodings:
                    # для каждой кодировки определяем знакомо ли лицо
                    person = Face.by_encoding(face_encoding)

                    # Если знакомо
                    if person:
                        # если давно не виделись
                        if not person.recently_seen:
                            # Поприветствовать лицо
                            person.hello()
                        # обозначить, что увиделись
                        person.see_you()

                    # если лицо не знакомо
                    else:
                        person = Face.save_encoding(face_encoding)
                        height, width = frame.shape[:2]
                        # рассмотреть лицо и спросить имя
                        name = examine_face(height, width, face_locations)
                        if name:
                            Face.make_friends(face_encoding, name)

                print(frame_count)

            frame_count += 1

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
