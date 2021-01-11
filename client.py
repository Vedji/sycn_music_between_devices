import socket, pickle

HOST = '192.168.1.31'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

data = {
    'name': 'LarMoV - Пароль ТЕТРИАНДОХ.mp3',
    'value': []
}


file = open('client/LarMoV - Пароль ТЕТРИАНДОХ.mp3', 'rb')

k = True
while k:
    k = file.read(1000)
    data['value'].append(k)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(data))
s.close()
