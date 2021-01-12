import socket
import os
import time
import json

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
PATHTOMUSIC = 'mus\\'
SAVEFOLDERSLOCATION = True

music = b''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server ip: ', HOST)
s.bind((HOST, PORT))
s.listen()


def save_music_to_file(music_info: dict) -> None:
    path = PATHTOMUSIC
    if SAVEFOLDERSLOCATION:
        path = path + music_info['path']
    if not os.path.exists(path):
        os.makedirs(path)
    file = open(path + music_info['name'], 'wb')
    file.write(bytearray(music_info['value']))
    file.close()
    print('Music {}, save. '.format(music_info['name']))


while True:
    conn, addr = s.accept()
    start_time = time.time()
    print('Connected by', addr)
    fl = True
    received_data = ''
    while fl:
        received_data += conn.recv(1).decode('utf-8')
        if '|infofs|' in received_data:
            fl = False
    received_data = received_data[received_data.find('|infost|') + 8: received_data.find('|infofs|')]
    len_music_array = [0, int(json.loads(received_data))]
    _data = ''
    flag = True
    while flag and conn.getblocking():
        fl = False
        received_data = ''

        if flag and not fl:
            conn.send(b'|_send_|')
            _data += conn.recv(8).decode('utf-8')

        if not fl and '|start_|' in _data:
            fl = True
            print('Передача Музыкальной композиции начата. ')
            _data = _data[_data.find('|start_|') + 8:]

        while fl:
            _data += conn.recv(134217728).decode('utf-8')
            if '|finish|' in _data:
                received_data = _data[:_data.find('|finish|')]
                _data = _data[_data.find('|finish|') + 8:]
                fl = False
                len_music_array[0] += 1
                # Здесь сохраняем музло
                save_music_to_file(json.loads(received_data))
                print('Получено: ', len(json.loads(received_data)['value']))
                print('Файл ({}/{}) получен'.format(len_music_array[0], len_music_array[1]))

        if not fl and '|thatal|' in _data:
            flag = False
            _data = ''
            print('Передача Музыки завершенна. ')
            conn.send(b'|close_|')

    # print(json.loads(received_data))

    print(' Write music Finished. ', end='')
    print("--- %s seconds ---" % (time.time() - start_time))
    print('Client {} processed. '.format(addr))
