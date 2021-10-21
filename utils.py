import os
import numpy as np
from faces import Face

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


