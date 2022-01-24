import socket

HOST = '127.0.0.1' # the name or IP address of the server
PORT = 4000 # port used by server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'HEllo World')
    data = s.recv(1024)

print('Received ', repr(data))