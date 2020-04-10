from client_src.game import *
from settings_reader import *

# PARAMETRI
TIMEOUT = 0.2

# leggo i settings dal file e se non ci sono li chiedo all'utente
settings = leggi_prop(['server_ip', 'server_port'])

if settings[0] == '':  # server_ip
    ipServer = input('ip: ')
else:
    ipServer = settings[0]
if settings[1] == '':  # server_port
    portaServer = int(input('porta: '))
else:
    portaServer = int(settings[1])

ADDRESS_SERVER = (ipServer, portaServer)
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
nCol = int(messInizia.get_val('n_col'))
nRig = int(messInizia.get_val('n_rig'))
dimTavola = (nCol, nRig)

clientSocket.settimeout(TIMEOUT)

gameIstance = Game(inizia, clientSocket, dimTavola)
gameIstance.run()
