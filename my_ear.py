import json
import os
import pyaudio
from vosk import Model, KaldiRecognizer

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


# def listen_always():
#     while Avatar.listening:
#         print('I listen')
#         data = stream.read(4000, exception_on_overflow=False)
#         if len(data) == 0:
#             break
#         if rec.AcceptWaveform(data):
#             x = json.loads(rec.Result())
#
#             return x['text']


def listen(listening):
    if listening:
        stream.start_stream()
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            return False

        if rec.AcceptWaveform(data) and listening:
            text = json.loads(rec.Result())['text']
            stream.stop_stream()
            return text
