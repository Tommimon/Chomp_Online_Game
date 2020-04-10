from game import *

# PARAMETRI
IP_SERVER = 'localhost'
PORTA_SERVER = 50000


ADDRESS_SERVER = (IP_SERVER, PORTA_SERVER)
clientSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
clientSocket.connect(ADDRESS_SERVER)
mess_inizia = Messaggio()
mess_inizia.recv(clientSocket)
inizia = mess_inizia.get_var('inizia')
print(inizia)
inizia = inizia == 'True'   # se il messaggio dice 'True' allora devo iniziare
print(inizia)

gameIstance = Game(inizia, clientSocket)
gameIstance.run()
