import face_recognition
import cv2

import speech
from utils import read_face_encodings, write_face_encoding
from faces import Face


if __name__ == '__main__':
    read_face_encodings()
    face_locations = []

    frame_count = 0
    process_every_frame = 5

    # Получить ссылку на вебкамеру (#0 - камера по умолчанию)
    # image_source = 0
    camera_ip = '192.168.1.15'
    image_source = f'rtsp://{camera_ip}/live/ch00_0'

    # # Получить поток с IP камеры
    video_capture = cv2.VideoCapture(image_source)

    while video_capture.isOpened():
        person = None
        # Захват единичного кадра видео
        ret, frame = video_capture.read()

        if ret:
            # Обработка кадров через один для ускорения процесса
            if frame_count % process_every_frame == 0:
                print('frame ', frame_count)
                # Уменьшение размеров кадра для более быстрого распознавания (если что)
                scale = 0.5
                small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

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
                            speech.speak(f'Здравствуй, {person.name}')
                            print(f'Здравствуй, {person.name}')
                            person.see_you()
                    else:
                        print('unknown face')
                        # move face location to the center of the frame
                        # ask for name
                        # move face nearest to the center to the center
                        # listen for a name
                        # instantiate a face and write down face parameters
                        ...

            frame_count += 1
