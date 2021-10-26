import json
import os

import pyaudio
from vosk import Model, KaldiRecognizer

import my_ear
from models import Avatar


model_name = 'model_small'
if not os.path.exists(model_name):
    print(
        "Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as "
        "'model' in the current folder.")
    exit(1)


model = Model(model_name)
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

if __name__ == '__main__':
    while True:
        text = my_ear.listen(Avatar.listening)
        if text:
            if 'аня повтори' in text:
                text = text.replace('аня повтори', '')
                Avatar.voice = 'Anna+CLB'
            elif 'александр повтори' in text:
                text = text.replace('александр повтори', '')
                Avatar.voice = 'aleksandr'
            Avatar.say(text)
