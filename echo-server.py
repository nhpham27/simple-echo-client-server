import socket

HOST = '127.0.0.1' # local host
PORT = 4000 # port to listen to

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # associate the socket with a specific network interface and port number
    s.listen() # enable the server to accept connections
    conn, addr = s.accept() # block and wait for connection
    with conn:
        print('Connected by ', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

