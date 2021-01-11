import socket
import pickle
import os
import time

HOST = '192.168.1.31'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
ALL_MUSIC_PATH = []
SUPPORTED_MUSIC_FORMATS = ('mp3', 'ogg')


def add_to_list(ls: list, ad: str, left_add: bool = True) -> None:
    for i in range(len(ls)):
        if left_add:
            ls[i] = ad + ls[i]
        else:
            ls[i] = ls[i]+  ad


def music_serialization(name: str, path: str) -> bytes:
    """ Return serialized dict(name, path, file)"""
    file = open(path + name, 'rb')
    print(name, path, sep=', ')
    data = {
        'name': name,
        'path': path,
        'value': b''
    }
    k = file.read(1000000)
    while k:
        data['value'] += k
        k = file.read(1000000)
    data['value'] += k
    return pickle.dumps(data)


def brute_force_music_path() -> list:
    paths = []
    music_files = []
    for c in os.listdir(path='.'):
        if os.path.isdir(c):
            paths.append(c + '\\')
        elif os.path.isfile(c) and c.split('\\')[-1].split('.')[-1] in SUPPORTED_MUSIC_FORMATS:
            music_files.append(c)

    while paths:
        cur = paths.pop(0)
        buff = os.listdir(path=cur)
        for c in buff:
            if os.path.isdir(cur + c):
                paths.append(cur + c + '\\')
            elif os.path.isfile(cur + c) and c.split('.')[-1] in SUPPORTED_MUSIC_FORMATS:
                music_files.append(music_serialization(c, cur))
    return music_files

start_time = time.time()

musicals_files = brute_force_music_path()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(pickle.dumps(musicals_files))
print(len(pickle.dumps(musicals_files)))
s.close()
print("--- %s seconds ---" % (time.time() - start_time))
