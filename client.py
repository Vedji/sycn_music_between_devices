import socket
import pickle
import os
import time
import json


HOST = '192.168.1.31'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
ALL_MUSIC_PATH = []
SUPPORTED_MUSIC_FORMATS = ('mp3', 'ogg')
MUSICUPLOADINGPATH = ''


def add_to_list(ls: list, ad: str, left_add: bool = True) -> None:
    for i in range(len(ls)):
        if left_add:
            ls[i] = ad + ls[i]
        else:
            ls[i] = ls[i] + ad


def music_serialization(name: str, path: str) -> dict:
    """ Return serialized dict(name, path, file)"""
    print(name, path, sep=', ')
    file = open(path + name, 'rb')
    value = file.read()
    file.close()
    data = {
        'name': name,
        'path': path,
        'value': list(value)
    }
    print(len(data['value']))
    return data


def brute_force_music_path() -> list:
    paths = []
    music_files = []
    for c in os.listdir(MUSICUPLOADINGPATH if MUSICUPLOADINGPATH else '.'):
        if os.path.isdir(MUSICUPLOADINGPATH + c):
            paths.append(MUSICUPLOADINGPATH + c + '\\')
        elif os.path.isfile(MUSICUPLOADINGPATH + c) and c.split('\\')[-1].split('.')[-1] in SUPPORTED_MUSIC_FORMATS:
            music_files.append(MUSICUPLOADINGPATH + c)

    while paths:
        cur = paths.pop(0)
        buff = os.listdir(path=cur)
        for c in buff:
            if os.path.isdir(cur + c):
                paths.append(cur + c + '\\')
            elif os.path.isfile(cur + c) and c.split('.')[-1] in SUPPORTED_MUSIC_FORMATS:
                music_files.append((c, cur))
    return music_files


start_time = time.time()

music_paths = brute_force_music_path()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


s.send(b'|infost|')
s.send(str.encode(json.dumps(len(music_paths))))
s.send(b'|infofs|')


# s.sendall(b'|start_|' + str.encode(json.dumps(data)) + b'|finish|')

_data = ''
while music_paths:
    _data += s.recv(8).decode('utf-8')
    flag = False
    if'|_send_|' in _data:
        _data = _data[_data.find('|_send_|') + 8:]
        flag = True
    if flag:
        flag = False
        current_music_file = music_paths.pop(0)
        s.send(b'|start_|')
        s.send(str.encode(json.dumps(music_serialization(current_music_file[0], current_music_file[1]))))
        s.send(b'|finish|')
s.send(b'|thatal|')
_data += s.recv(8).decode('utf-8')
while '|close_|' not in _data:
    _data += s.recv(8).decode('utf-8')
s.close()
print("--- %s seconds ---" % (time.time() - start_time))
