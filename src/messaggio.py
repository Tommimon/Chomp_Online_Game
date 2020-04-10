import socket as sock

# PARAMETRI
CODIFICA = 'utf-8'
BUFFER_SIZE = 2048


class Messaggio:
    def __init__(self):
        self.stringa = ''

    def add_val(self, nome, valore):
        nuovo = nome + '=' + str(valore) + '\n'
        self.stringa = self.stringa + nuovo

    def get_val(self, nome):
        try:
            stringa_var = self.stringa
            stringa_var = stringa_var[stringa_var.index(nome):]  # tolgo tutta la parte prima che non serve
            stringa_var = stringa_var[:stringa_var.index('\n')]  # adesso che ho tagliato il primo \n è quello che serve
            stringa_var = stringa_var[stringa_var.index('=') + 1:]  # tolgo il nome della var
            return stringa_var
        except ValueError:
            return None

    def set_val(self, nome, valore):
        try:
            prec_stringa = self.stringa
            prec_stringa = prec_stringa[prec_stringa.index(nome):]
            prec_stringa = prec_stringa[:prec_stringa.index('\n')]  # come sopra così pendo 'nome=val_prec'
            new_stringa = nome + '=' + str(valore)
            self.stringa = self.stringa.replace(prec_stringa, new_stringa)
            return True
        except ValueError:
            return False

    def send(self, socket):
        socket.send(self.stringa.encode(CODIFICA))

    def safe_send(self, socket):
        try:
            self.send(socket)
        except ConnectionAbortedError or ConnectionResetError:  # occore quando provo a mandare a uno che ha chiuso
            pass

    def recv(self, socket):
        self.stringa = socket.recv(BUFFER_SIZE).decode(CODIFICA)

    def try_recv(self, socket):
        try:
            self.stringa = socket.recv(BUFFER_SIZE).decode(CODIFICA)
            return True
        except sock.timeout:
            return False

    def reset(self):
        self.stringa = ''
