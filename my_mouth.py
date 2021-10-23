import os


def say(text):
    voice = 'anna'
    s = f'echo "{text}" | RHVoice-test -p {voice}'
    return os.popen(s)
