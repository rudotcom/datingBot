import sqlite3
# ######## PATH ##########
enc_path = 'encodings'  # Файлы с кодом лиц


# ######## CAMERA ########
#       Получить ссылку на вебкамеру (#0 - камера по умолчанию)
image_source = 0
#       Получить ссылку на IP камеру
# camera_ip = '192.168.1.15'
# image_source = f'rtsp://{camera_ip}/live/ch00_0'

remember_seconds = 7200


PHRASES = {
    'make_friends': ['Меня зовут Мурзилка, а тебя?', 'Как тебя зовут?',
                     'Давай познакомимся. Меня зовут Мурзилка, а тебя?'],
    'come_closer': ['Подойди поближе пожалуста', 'Ближе, не бойся', 'Ближе', 'Чуть ближе', '', '', '', ],
    'my_name_is': ['а меня', 'меня', 'зовут', 'моё имя', 'меня звать', ],
}


conn = sqlite3.connect("faces.sqlite3")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
