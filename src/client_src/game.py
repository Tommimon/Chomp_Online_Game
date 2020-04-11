from client_src.tavola import *
from client_src.globale import *
from messaggio import *
from bottone import *

# PARAMETRI
FPS = 60  # Frames per second.
RISOLUZIONE = (720, 480)
POS_TAVOLA = (RISOLUZIONE[0]/10, RISOLUZIONE[1]/10)
SIZE_TAVOLA = (RISOLUZIONE[0]*0.8, RISOLUZIONE[1]*0.8)  # ho scalato un po' la risoluzione dello schermo
DIM_TAVOLA = (10, 4)  # numero di caselle in goni direzione
NERO = (0, 0, 0)
ROSSO = (250, 0, 0)
VERDE = (0, 250, 0)
PADDING = 4


class Game:  # gestisce code degli eventi, game loop e aggiornamento dello schermo e comunicazione server_src
    def __init__(self, inizia, my_socket, dim_tavola):
        succes, fail = pg.init()
        self.screen = pg.display.set_mode(RISOLUZIONE)  # mostro schermo
        pg.display.set_caption('Chomp')
        self.clock = pg.time.Clock()  # inizializzo clock
        self.socket = my_socket  # da usare per mandare e ricevere
        self.state = GameState(inizia, dim_tavola)
        self.running = True
        self.rivincita = False
        Globale.game = self  # verrà usata come varibile globale (sicome statica posso accedere da ovunque)
        print('inizia il gioco!')

    def run(self):  # fa il game loop
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            if not self.state.finePartita:
                self.ceck_server()
            for event in pg.event.get():
                self.resolve_event(event)
            self.update_screen()
        return self.rivincita  # restituisco al client True se voglio fare un'altra partita

    def resolve_event(self, event):
        if event.type == pg.QUIT:
            self.quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.state.mouse_click(event.pos)

    def update_screen(self):
        self.screen.fill(NERO)  # copro frame prec
        self.state.display(self.screen)  # disegno tutto quello che riguarda lo stato attuale
        pg.display.update()  # Or pg.display.flip()

    def send_move(self, x, y):  # arrivo qui solo da mouse_click quindi posso giocare e non è finita la partita
        self.state.possoGiocare = False  # devo aspettare per giocare
        mossa = Messaggio()
        mossa.add_val('x', x)
        mossa.add_val('y', y)
        mossa.send(self.socket)

    def ceck_server(self):  # controlla se sono arrivati messaggi dal server
        mossa = Messaggio()
        risp = mossa.try_recv(self.socket)  # controllo se arriva risposta
        if risp:  # è vero se è arrivato qualcosa
            if mossa.get_val('quit') is not None:  # arrivato messaggio che l'avversario ha quittato
                self.abbandono()
                return
            if mossa.get_val('opponent') is not None:
                self.state.possoGiocare = self.state.turnoMio  # dopo che trovi avversario se inizi tu allora pui giocar
                return
            x = int(mossa.get_val('x'))
            y = int(mossa.get_val('y'))
            win = mossa.get_val('win')
            self.state.del_caselle(x, y)
            if win != 'None':  # se arriva messaggio che è finita
                self.state.win = win == 'True'  # win diventa True se era 'True' se no False
                self.fine_partita(self.state.win)

    def fine_partita(self, win):  # mi occupereò di chiudere il socket nel client
        if win:
            print('HAI VINTO!')
        else:
            print('HAI PERSO')
        self.state.finePartita = True

    def abbandono(self):  # quando l'avversario abbandona
        print("l'avversario ha abbandonato")
        self.state.win = True
        self.fine_partita(True)

    def quit(self):  # mi occupereò di chiudere il socket nel client
        self.running = False


class GameState:  # contiene tutte le var significative per descrivere il gioco e i metodi secondo cui modificarle
    def __init__(self, inizia, dim_tavola):
        self.tavoletta = Tavola(POS_TAVOLA, SIZE_TAVOLA, dim_tavola, PADDING)
        self.tavoletta.crea_caselle()
        self.possoGiocare = False  # quando clicko una cella diventa false e quando l'altro gioca diventa true
        self.turnoMio = inizia
        self.finePartita = False
        self.win = None
        self.bottone_quit = Bottone('Quit', (50, RISOLUZIONE[1] - 32), bg_color=ROSSO)
        self.bottone_rivincita = Bottone('Rivincita', (150, RISOLUZIONE[1] - 32), bg_color=VERDE)
        self.top_text = Bottone('', (100, 5), bg_color=NERO)  # uso un bottone come testo per non fare una classe testo

    def mouse_click(self, pos):
        if self.finePartita:
            if self.bottone_rivincita.ceck_click(pos):
                Globale.game.rivincita = True
                Globale.game.quit()
            elif self.bottone_quit.ceck_click(pos):
                Globale.game.quit()
        else:
            if self.possoGiocare:
                self.tavoletta.ceck_click(pos)

    def del_caselle(self, x, y):
        self.turnoMio = not self.turnoMio
        self.possoGiocare = self.turnoMio  # se prima non era il mio turno adesso posso giocare
        self.tavoletta.del_caselle(x, y)

    def display(self, screen):
        self.tavoletta.blit(screen)
        if self.finePartita:
            self.display_fine(screen)
            self.bottone_rivincita.blit(screen)
            self.bottone_quit.blit(screen)
        else:
            self.display_turno(screen)

    def display_turno(self, screen):
        if self.possoGiocare:
            self.top_text.text = 'Tocca a te'
            self.top_text.text_color = VERDE
        else:
            self.top_text.text = "In attesa dell'avversario"
            self.top_text.text_color = ROSSO
        self.top_text.blit(screen)

    def display_fine(self, screen):
        if self.win:
            self.top_text.text = 'Hai vinto!'
            self.top_text.text_color = VERDE
        else:
            self.top_text.text = 'Hai Perso'
            self.top_text.text_color = ROSSO
        self.top_text.blit(screen)
