from game import *

# PARAMETRI
CODIFICA = 'utf-8'
BUFFER_SIZE = 2048
IP_SERVER = 'localhost'
PORTA_SERVER = 50000


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
clientSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
clientSocket.connect(ADDRESS_SERVER)
iniziaString = clientSocket.recv(BUFFER_SIZE).decode()
inizia = iniziaString == 'True'  # se la stringa è 'True' allora devo iniziare se no no

gameIstance = Game(inizia, clientSocket)
gameIstance.run()
