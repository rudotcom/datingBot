import face_recognition
import cv2
from utils import read_face_encodings, examine_face
from faces import Face
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
            # Обработка кадров через один для ускорения процесса
            if frame_count % process_every_frame == 0:
                # Уменьшение размеров кадра для более быстрого распознавания (если что)
                scale = 1
                small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
                height, width = small_frame.shape[:2]

                # Конвертация изображения из цветов BGR (которые испоользует OpenCV)
                # в цвета RGB (которые использует face_recognition)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Найти все лица и их кодировки в текущем кадре видео
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    person = Face.by_encoding(face_encoding)

                    if person:
                        if not person.recently_seen:
                            person.hello()
                        person.see_you()
                    else:
                        name = examine_face(height, width, face_locations)
                        if name:
                            Face.make_friends(face_encoding, name)

                print(frame_count)

            frame_count += 1
