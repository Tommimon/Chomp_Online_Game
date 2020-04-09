import socket as sock


def is_mossa(stringa):
    return True


def broadcast(message):
    g1Socket.send(message)
    g2Socket.send(message)


# PARAMETRI
CODIFICA = 'utf-8'
BUFFER_SIZE = 2048
IP_SERVER = 'localhost'
PORTA_SERVER = 50000


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
serverSocket.bind(ADDRESS_SERVER)
serverSocket.listen()
print('server pronto')

g1Socket, g1Address = serverSocket.accept()
print('connesso g1', g1Address)
g1Socket.send('True'.encode(CODIFICA))

g2Socket, g2Address = serverSocket.accept()
print('connesso g2', g2Address)
g2Socket.send('False'.encode(CODIFICA))

turnoG1 = True

while True:
    if turnoG1:
        messaggio = g1Socket.recv(BUFFER_SIZE)
    else:
        messaggio = g2Socket.recv(BUFFER_SIZE)

    copy = messaggio
    print(copy.decode(CODIFICA))
    if is_mossa(messaggio):
        # qui devo segnarmi la mossa lato server
        broadcast(messaggio)

    turnoG1 = not turnoG1
