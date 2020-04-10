from messaggio import *
from server_src.tavola import *


def leggi_mossa(mossa):  # prende in input un Messaggio
    x = int(mossa.get_val('x'))
    y = int(mossa.get_val('y'))
    return x, y  # aggiungere try + except tipo non int


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
DIM_TAVOLA = (10, 4)  # numero di caselle in ogni direzione


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
serverSocket.bind(ADDRESS_SERVER)
serverSocket.listen()
print('server_src pronto')


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
tavola = Tavola(DIM_TAVOLA)

while True:
    richiesta = Messaggio()
    if turnoG1:
        print('waiting g1...')
        richiesta.recv(g1Socket)
    else:
        print('waiting g2...')
        richiesta.recv(g2Socket)

    print('ricevuto:', richiesta.stringa)
    xMossa, yMossa = leggi_mossa(richiesta)
    if tavola.ceck_mossa(xMossa, yMossa):  # dovrei anche controllare che la mossa stia dentro alla tabella
        print('mossa verificata:', xMossa, yMossa)
        tavola.del_caselle(xMossa, yMossa)
        winMossa = None  # dovrei controllare se ho finito, None significa che nessuno ha vinto
        risposta = scrivi_mossa(xMossa, yMossa, winMossa)
        print('sending:', risposta.stringa)
        broadcast(risposta)
        turnoG1 = not turnoG1

