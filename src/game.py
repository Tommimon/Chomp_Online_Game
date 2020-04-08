from src.tavola import *

# PARAMETRI
FPS = 60  # Frames per second.
RISOLUZIONE = (720, 480)
NERO = (0, 0, 0)
PADDING = 4
DELCASELLE = pg.USEREVENT + 3  # significa che il server ha detto quali caselle vanno tolte


class Game:  # gestisce code degli eventi, game loop e aggiornamento dello schermo e comunicazione server
    def __init__(self, inizia):
        succes, fail = pg.init()
        print("{0} successes and {1} failures".format(succes, fail))
        self.state = GameState(inizia)
        self.screen = pg.display.set_mode(RISOLUZIONE)  # mostro schermo
        self.clock = pg.time.Clock()  # inizializzo clock
        self.running = True

    def run(self):  # fa il game loop
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            self.ceck_server()
            for event in pg.event.get():
                self.resolve_event(event)
            self.update_screen()

    def resolve_event(self, event):
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.state.mouse_click(event.pos)
        elif event.type == CLICKCASELLA:
            self.state.possoGiocare = False  # devo aspettare per giocare
            pass  # dobbiamo inviare al server la richiesta di togliere una casella
        elif event.type == DELCASELLE:
            self.state.del_caselle(event.x, event.y)
        elif event.type == FINEPARTITA:
            print('fine, ha vinto il ' + event.win + ' giocatore')

    def update_screen(self):
        self.screen.fill(NERO)  # copro frame prec
        self.state.display(self.screen)  # disegno tutto quello che riguarda lo stato attuale
        pg.display.update()  # Or pg.display.flip()

    def ceck_server(self):  # controlla se sono arrivati messaggi dal server
        pass  # controllo se arriva risposta
        pg.event.post(DELCASELLE)  # manca specificare quali caselle


class GameState:  # contiene tutte le var significative per descrivere il gioco e i metodi secondo cui modificarle
    def __init__(self, inizia):
        self.tavoletta = Tavola(0, 0, 720, 480, 10, 4, PADDING)
        self.tavoletta.crea_caselle()
        self.possoGiocare = inizia  # quando clicko una cella diventa false e quando l'altro gioca diventa true
        self.turnoMio = inizia

    def mouse_click(self, pos):
        if self.possoGiocare:
            self.tavoletta.ceck_click(pos)

    def del_caselle(self, x, y):
        self.turnoMio = not self.turnoMio
        self.possoGiocare = self.turnoMio  # se prima non era il mio turno adesso posso giocare
        self.tavoletta.del_caselle(x, y)

    def display(self, screen):
        self.tavoletta.blit(screen)

