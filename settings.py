import sqlite3
import os.path
# ######## PATH ##########
enc_path = 'encodings'  # Файлы с кодом лиц


# ######## CAMERA ########
#       Получить ссылку на вебкамеру (#0 - камера по умолчанию)
image_source = 0
#       Получить ссылку на IP камеру
# camera_ip = '192.168.1.15'
# image_source = f'rtsp://{camera_ip}/live/ch00_1'

remember_seconds = 7200
AVATAR_NAME = 'Неваляшка'

PHRASES = {
    'hello': ['Здравствуй', 'Привет', 'Как дела', 'рада тебя видеть'],
    'make_friends': [f'Меня зовут {AVATAR_NAME}, а тебя?', 'Как тебя зовут?',
                     f'Давай познакомимся. Меня зовут {AVATAR_NAME}, а тебя?'],
    'come_closer': ['Подойди поближе пожалуста', 'Ближе, не бойся', 'Ближе', 'Чуть ближе'],
    'my_name_is': ['а меня', 'меня', 'зовут', 'моё имя', 'меня звать', ],
    'your_name_is': ['тебя зовут', 'твое имя', '', ],
    'is_your_name': ['правильно?', 'я правильно услышала?', 'так?', 'это верно?'],
    'positive': ['верно', 'правильно', 'да', 'конечно', 'безусловно', 'права', 'так', 'всё'],
}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

db_file = os.path.join(BASE_DIR, "faces.sqlite3")
if not os.path.exists(db_file):
    # Создание таблицы бд если файла нет
    init = sqlite3.connect(db_file)
    cursor = init.cursor()
    cursor.execute("CREATE TABLE faces (name text, encoding BLOB)")
    init.commit()
    init.close()

conn = sqlite3.connect(db_file)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

