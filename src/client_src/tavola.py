import pygame as pg
from client_src.globale import *

MARRONE = (139, 69, 13)
ROSSO = (255, 0, 0)


class Casella:
    def __init__(self, index, pos, lato, avvelenato):
        self.index_x = index[0]  # è la poszione che la casella occupa enlla tavola (è un num naturale)
        self.index_y = index[1]
        self.rect = pg.Rect(pos, (lato, lato))
        self.image = pg.Surface((lato, lato))
        if avvelenato:
            self.image.fill(ROSSO)
        else:
            self.image.fill(MARRONE)

    def blit(self, screen):
        screen.blit(self.image, self.rect)

    def ceck_click(self, pos):  # se clicco la casella chiamo del_caselle sulla tavola "madre"
        if self.rect.collidepoint(pos):  # da una warning perché non sa che è una tupla (sto scemo)
            Globale.game.send_move(self.index_x, self.index_y)


class Tavola:
    def __init__(self, pos, size, dimensione, padding):
        self.pos_x = pos[0]  # posizione in pixel (distanza sa bordo sinistro)
        self.pos_y = pos[1]
        self.width = size[0]  # larghezza in pixel
        self.height = size[1]
        self.n_col = dimensione[0]  # numero di colonne
        self.n_rig = dimensione[1]
        self.lato = 0
        self.padding = padding
        self.margine_left = 0  # margine che devo lasciare per centrare la tavola nello spazio che mi è dato
        self.margine_top = 0
        self.righe = []  # lista organizzata in righe

    def _trova_lato(self):  # trova le dimensioni adatte per riempire lo spazio dato e centrare la tabella
        lato_x = self.width // self.n_col  # la divisione intera arrotonda per troncamento
        lato_y = self.height // self.n_rig
        if lato_x > lato_y:
            self.lato = lato_y  # se tolgo il padding ora viene la tavola della dim giusta
        else:
            self.lato = lato_x
        self.margine_left = (self.width - (self.lato * self.n_col)) / 2  # prendo la metà dello spazio vuoto
        self.margine_top = (self.height - (self.lato * self.n_rig)) / 2
        self.lato -= self.padding  # devo togliere il padding altrimenti quando disengo viene troppo grande

    def crea_caselle(self):  # crea tutte le casella nella poszione giusta e le aggiunge alla lista caselle
        self._trova_lato()
        y = self.pos_y + self.margine_top
        for i in range(0, self.n_rig):
            x = self.pos_x + self.margine_left
            rig = []
            for j in range(0, self.n_col):
                if i == self.n_rig - 1 and j == 0:  # se è la casella in basso a sinistra metto avvelenato = True
                    avvelenato = True
                else:
                    avvelenato = False
                new = Casella((j, i), (x, y), self.lato, avvelenato)
                rig.append(new)  # aggiungo all lista a righe
                x += self.lato + self.padding
            y += self.lato + self.padding
            self.righe.append(rig)

    def blit(self, screen):
        for rig in self.righe:
            for cas in rig:
                cas.blit(screen)

    def ceck_click(self, pos):
        for rig in self.righe:
            for cas in rig:
                cas.ceck_click(pos)

    def del_caselle(self, x, y):
        for i in range(0, len(self.righe)):
            if i <= y:  # se sono abbastanza in alto
                rig = self.righe[i]
                rig = rig[0:x]  # tolgo tutti quelli da x in poi, x compreso
                self.righe[i] = rig

    # questo va fatto lato server_src perché va controllato
    # def _ceck_win(self):  # controllo se sono finite le caselle o se ne manca una
    #     if len(self.righe[self.n_rig - 1]) == 0:  # se la riga più bassa è vuota allora sognifica che è tutto vuoto
    #         # l'ultimo che ha giocato ha perso
    #         Globale.game.fine_partita('penultimo')
    #     elif len(self.righe[self.n_rig - 1]) == 1 and (self.n_rig == 1 or len(self.righe[self.n_rig - 2]) == 0):
    #         # devo controllare che la riga più bassa abbia 1 solo elemento e che la penultima 0 (se c'è)
    #         # l'ultimo che ha giocato ha vinto
    #         Globale.game.fine_partita('ultimo')
