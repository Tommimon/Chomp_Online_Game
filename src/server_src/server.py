from messaggio import *
from server_src.tavola import *

# PARAMETRI
IP_SERVER = '192.168.1.100'
PORTA_SERVER = 46142
DIM_TAVOLA = (10, 4)  # numero di caselle in ogni direzione


def leggi_mossa(mossa):  # prende in input un Messaggio
    try:
        x = int(mossa.get_val('x'))
        y = int(mossa.get_val('y'))
        return x, y
    except TypeError:
        # probabilemte significa che uno ha quittato e non ho ricevuto risposta abbandono() dovrebbe essere già andato
        return None, None
    except ValueError:
        # il client ha mandato mossa incrompensibile, retituendo None non cerrà accettata da ceck_mossa
        return None, None


def manda_risposta(x, y, win):
    risposta = scrivi_mossa(x, y)
    if win == 'ultimo':
        win = turnoG1  # se ha vinto l'ultimo allora win deve valere il giocatore che sta giocando
    elif win == 'penultimo':
        win = not turnoG1
    else:
        win = None

    risposta.add_val('win', win)
    print('sending to g1:', risposta.stringa)
    risposta.safe_send(g1Socket)

    if win is not None:  # se non è None inverto il valore di win, se è None è uguale per entrambi i giocatori
        risposta.set_val('win', not win)
    print('sending to g2:', risposta.stringa)
    risposta.safe_send(g2Socket)


def scrivi_mossa(x, y):  # restituisce un Messaggio
    mossa = Messaggio()
    mossa.add_val('x', x)
    mossa.add_val('y', y)
    return mossa


def abbandono(is_g1):
    messaggio = Messaggio()
    messaggio.add_val('quit', True)
    if is_g1:
        messaggio.safe_send(g2Socket)
    else:
        messaggio.safe_send(g1Socket)
    global partitaInCorso
    partitaInCorso = False


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
serverSocket.bind(ADDRESS_SERVER)
serverSocket.listen()

while True:
    print('server_src pronto')
    messInizia = Messaggio()
    g1Socket, g1Address = serverSocket.accept()
    print('connesso g1', g1Address)
    messInizia.add_val('inizia', True)
    messInizia.add_val('n_col', DIM_TAVOLA[0])
    messInizia.add_val('n_rig', DIM_TAVOLA[1])
    messInizia.send(g1Socket)  # gli dico se è lui a fare la prima mossa

    g2Socket, g2Address = serverSocket.accept()
    print('connesso g2', g2Address)
    messInizia.set_val('inizia', False)
    messInizia.send(g2Socket)

    partitaInCorso = True
    turnoG1 = True
    tavola = Tavola(DIM_TAVOLA)

    while partitaInCorso:
        richiesta = Messaggio()
        if turnoG1:
            print('waiting g1...')
            try:
                richiesta.recv(g1Socket)
            except ConnectionAbortedError:
                abbandono(True)  # True significe che il G1 ha abbandonato
        else:
            print('waiting g2...')
            try:
                richiesta.recv(g2Socket)
            except ConnectionAbortedError:
                abbandono(False)  # False significe che il G2 ha abbandonato

        print('ricevuto:', richiesta.stringa)
        xMossa, yMossa = leggi_mossa(richiesta)
        if tavola.ceck_mossa(xMossa, yMossa):  # dovrei anche controllare che la mossa stia dentro alla tabella
            print('mossa verificata:', xMossa, yMossa)
            tavola.del_caselle(xMossa, yMossa)  # elmina lato server le caselle che servono
            winMossa = tavola.ceck_win()  # None significa che non è finita la partita
            if winMossa is not None:
                partitaInCorso = False
            manda_risposta(xMossa, yMossa, winMossa)  # calcola i valori di win giusti per ogni giocatore e manda risp
            turnoG1 = not turnoG1  # adesso tocca all'altro
            print('tavola', tavola.righe)
        else:
            abbandono(turnoG1)  # il giocatore sta mandando mosse non valide

    print('fine partita')
    g1Socket.close()
    g2Socket.close()
    print('restarting')

