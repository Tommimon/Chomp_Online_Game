from messaggio import *


def leggi_mossa(mossa):  # prende in input un Messaggio
    x = int(mossa.get_val('x'))
    y = int(mossa.get_val('y'))
    return x, y


def scrivi_mossa(x, y, win):  # restituisce un Messaggio
    mossa = Messaggio()
    mossa.add_val('x', x)
    mossa.add_val('y', y)
    mossa.add_val('win', win)
    return mossa


def broadcast(message):  # prende in input un Messaggio
    message.send(g1Socket)
    message.send(g2Socket)


# PARAMETRI
IP_SERVER = 'localhost'
PORTA_SERVER = 50000


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
serverSocket.bind(ADDRESS_SERVER)
serverSocket.listen()
print('server pronto')


messInizia = Messaggio()
g1Socket, g1Address = serverSocket.accept()
print('connesso g1', g1Address)
messInizia.add_val('inizia', True)
messInizia.send(g1Socket)  # gli dico se è lui a fare la prima mossa

g2Socket, g2Address = serverSocket.accept()
print('connesso g2', g2Address)
messInizia.reset()
messInizia.add_val('inizia', False)
messInizia.send(g2Socket)

turnoG1 = True

while True:
    richiesta = Messaggio()
    if turnoG1:
        richiesta.recv(g1Socket)
    else:
        richiesta.recv(g2Socket)

    print(richiesta.stringa)
    xMossa, yMossa = leggi_mossa(richiesta)
    if xMossa is not None and yMossa is not None:  # dovrei anche controllare che la mossa stia dentro alla tabella
        winMossa = None  # dovrei controllare se ho finito, None significa che nessuno ha vinto
        risposta = scrivi_mossa(xMossa, yMossa, winMossa)
        broadcast(risposta)
        turnoG1 = not turnoG1

