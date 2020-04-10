from messaggio import *


def is_mossa(stringa):
    return True


def leggi_mossa(stringa):
    pass


def scrivi_mossa(x, y, win):
    stringa = str((x, y)) + ';win=' + str(win) + ';'


def broadcast(message):
    g1Socket.send(message)
    g2Socket.send(message)


# PARAMETRI
IP_SERVER = 'localhost'
PORTA_SERVER = 50000


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
serverSocket.bind(ADDRESS_SERVER)
serverSocket.listen()
print('server pronto')


mess_inizia = Messaggio()
g1Socket, g1Address = serverSocket.accept()
print('connesso g1', g1Address)
mess_inizia.add_var('inizia', True)
mess_inizia.send(g1Socket)  # gli dico se è lui a fare la prima mossa

g2Socket, g2Address = serverSocket.accept()
print('connesso g2', g2Address)
mess_inizia.reset()
mess_inizia.add_var('inizia', False)
mess_inizia.send(g2Socket)

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

