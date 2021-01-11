import socket, pickle

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

music = b''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = True
    while data:
        data = conn.recv(1024)
        music += data
    music = pickle.loads(music)
    file = open('server/'+music['name'], 'wb')
    for i in music['value']:
        file.write(i)
    file.close()
    print('All')
