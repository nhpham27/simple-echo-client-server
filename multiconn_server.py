
def multiconn_server(HOST, PORT):    
    from cgitb import Hook
    import selectors
    import socket
    import types
    from tkinter.messagebox import NO

    sel = selectors.DefaultSelector()

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT)) # associate the socket with a specific network interface and port number
    lsock.listen() # enable the server to listen for connections
    print('listening on ', (HOST, PORT))
    lsock.setblocking(False) # do not block calls made to this socket
    # register the socket to be monitored with sel.select()
    # we want to read selectors.EVENT_READ
    # data is arbitrary data returned from sel.select()
    sel.register(lsock, selectors.EVENT_READ, data=None)

    # accept the connection, get the new socket object and register
    # it with the selector
    def accept_wrapper(sock):
        conn, addr = sock.accept() # should be ready to read
        print('accepted connection from ', addr )
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    def service_connection(key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024) # should be ready to read
            if recv_data: # if the socket receive data
                data.outb += recv_data
            else: # if not receiving data
                print('closing connection to ', data.addr)
                sel.unregister(sock) # unregister the socket from the selector
                sock.close() # close the socket
        if mask & selectors.EVENT_WRITE: # when the socket is ready for writing
            if data.outb: # if the data is available
                print('echoing ', repr(data.outb), ' to ', data.addr)
                sent = sock.send(data.outb) # send data to client
                data.outb = data.outb[sent:] # the sent bytes are removed from the send buffer

    while True:
        # block until there are sockets ready for I/O
        # return a list of (key, event) tuples, one for each socket
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # if key.data is None, it's from a listening socket
                # neet to accept() the 
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)