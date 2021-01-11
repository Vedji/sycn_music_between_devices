import socket
import pickle
import os
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 65432
PATHTOMUSIC = 'server\\'

music = b''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Server ip: ', HOST)
s.bind((HOST, PORT))
s.listen()
while True:
    start_time = time.time()

    conn, addr = s.accept()
    print('Connected by', addr)
    data = True
    while data:
        data = conn.recv(134217728)
        music += data
    music = pickle.loads(music)
    print('Get Music finished. ', end='')
    print("--- %s seconds ---" % (time.time() - start_time))
    start_time = time.time()
    while music:
        cmf = music.pop(0)
        music_data = pickle.loads(cmf)
        if not os.path.exists(PATHTOMUSIC + music_data['path']):
            os.makedirs(PATHTOMUSIC + music_data['path'])
        music_file = open(PATHTOMUSIC + music_data['path'] + music_data['name'], 'wb')
        music_file.write(music_data['value'])
    print(' Write music Finished. ', end='')
    print("--- %s seconds ---" % (time.time() - start_time))
    music = b''
    print('Client {} processed. '.format(addr))
