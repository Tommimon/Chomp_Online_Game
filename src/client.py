from game import *

INIZIA = True

clientSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

# fare roba connessione

gameIstance = Game(INIZIA, clientSocket)
gameIstance.run()
