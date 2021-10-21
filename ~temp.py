import os

import face_recognition
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# import speechd

# tts_d = speechd.SSIPClient('test')
# tts_d.set_output_module('rhvoice')
# tts_d.set_language('ru')
# tts_d.set_rate(50)
# tts_d.set_punctuation(speechd.PunctuationMode.SOME)
from faces import Face

os.chdir(os.path.dirname(os.path.realpath(__file__)))
# Используем Truetype для печати кириллицей.
fontpath = "fonts/16457.otf"
font = ImageFont.truetype(fontpath, 45)
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


if __name__ == '__main__':
    read_face_encodings()
    face_locations = []

    frame_count = 0
    process_every_frame = 5

    # Получить ссылку на вебкамеру #0 (ту что по умолчанию)
    # video_capture = cv2.VideoCapture(0)
    # # Получить поток с IP камеры
    ip_cam = '192.168.1.15'
    url = f'rtsp://{ip_cam}/live/ch00_0'
    video_capture = cv2.VideoCapture(url)

    while video_capture.isOpened():
        # Захват единичного кадра видео
        ret, frame = video_capture.read()
        img_pil = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_pil)
        if ret:
            # Уменьшение размеров кадра для более быстрого распознавания (если что)
            scale = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

            # Конвертация изображения из цветов BGR (которые испоользует OpenCV)
            # в цвета RGB (которые использует face_recognition)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Обработка кадров через один для ускорения процесса
            if frame_count % process_every_frame == 0:
                # Найти все лица и их кодировки в текущем кадре видео
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:

                    name = None
                    # Совпадает ли лицо с известными лицами
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                    # Если в known_face_encodings найдено совпадение, просто использовать первое.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    else:
                        continue
                        # Либо, Используем известное лицо с наименьшим расстоянием от нового лица
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)

                        if matches[best_match_index] and face_distances[best_match_index] > 0.69:
                            print('face distance:', face_distances[best_match_index])
                            name = known_face_names[best_match_index]
                        else:
                            for face_location in face_locations:
                                (top, right, bottom, left) = face_location
                                im_crop = img_pil.crop((left, top, right, bottom))
                                im_crop.save(f'trash/{datetime.datetime.now()}.jpg', quality=95)
                                # print(f'new face encoding: {face_encoding}')
                                # name = input('Имя:')
                                # write_person_encoding(name, face_encoding)


                    face_names.append(name)

                # process_this_frame = not process_this_frame

                # Отобразить результаты
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    # Scale back up face locations since the frame we detected in was scaled
                    top *= scale
                    right *= scale
                    bottom *= scale
                    left *= scale
                    top, right, bottom, left = map(int, [top, right, bottom, left])

                    # Нарисовать прямоугольник вокруг лица
                    if name:
                        # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (50, 220, 255), cv2.FILLED)
                        cv2.rectangle(small_frame, (left, top), (right, bottom), (100, 100, 100, 10), 2)
                        draw.text((left + 1, top - 65), name, font=font, fill=(0, 80, 255, 100))
                        draw.text((left, top - 66), name, font=font, fill=(255, 255, 255, 10))
                        frame = np.array(img_pil)
                        print(frame_count, name)
                        if name not in names_spoken:
                            # tts_d.speak(f'Здравствуй, {name}')
                            print(f'Здравствуй, {name}')
                            names_spoken.append(name)
                    else:
                        cv2.rectangle(small_frame, (left, top), (right, bottom), (100, 100, 100, 100), 2)
                        draw.text((left + 7, bottom - 5), 'Кто это?', font=font, fill=(0, 0, 0, 100))

            # Display the resulting image
            cv2.imshow('Video', small_frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame_count += 1
        else:
            continue

    # Release handle to the webcam
    # tts_d.close()
    video_capture.release()
    cv2.destroyAllWindows()
