from client_src.game import *

# PARAMETRI
IP_SERVER = 'localhost'
PORTA_SERVER = 50000
TIMEOUT = 0.2


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
clientSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
clientSocket.connect(ADDRESS_SERVER)

messInizia = Messaggio()
messInizia.recv(clientSocket)
inizia = messInizia.get_val('inizia')
inizia = inizia == 'True'   # se il messaggio dice 'True' allora devo iniziare
if inizia:
    print('giochi per primo')
else:
    print('giochi per secondo')

clientSocket.settimeout(TIMEOUT)

gameIstance = Game(inizia, clientSocket)
gameIstance.run()
