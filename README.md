```shell
pip install -r requirements.txt
```

## speech-dispatcher
https://github.com/brailcom/speechd


# Создание таблицы
import sqlite3
 
conn = sqlite3.connect("faces.sqlite3") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
 
cursor.execute("""CREATE TABLE faces
                  (name text, encoding BLOB)
               """)
 