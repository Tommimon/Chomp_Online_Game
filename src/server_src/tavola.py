
class Tavola:
    def __init__(self, dimensione):
        self.n_col = dimensione[0]  # numero di colonne
        self.n_rig = dimensione[1]
        self.righe = [self.n_col] * self.n_rig  # la tabella è rappresentata come una lista di righe
        # e ogni riga è identificata semplicemente dalla sua lunghezza

    def ceck_mossa(self, index_x, index_y):  # nota che entrano
        if index_x is not None and index_y is not None:  # significa che sono stati letti correttamente
            # se il mio index punta ad una casella che c'è ancora
            if self.righe[index_y] >= index_x+1:  # -1 perché quello è l'index della pos e lo confronto con la lunghezza
                return True
        return False

    def del_caselle(self, index_x, index_y):
        for i in range(0, len(self.righe)):
            if i <= index_y:  # se sono abbastanza in alto
                self.righe[i] = index_x  # tolgo tutti quelli da x in poi, x compreso

    def ceck_win(self):  # controllo se sono finite le caselle o se ne manca una
        if self.righe[self.n_rig - 1] == 0:  # se la riga più bassa è vuota allora sognifica che è tutto vuoto
            # l'ultimo che ha giocato ha perso
            return 'penultimo'
        elif self.righe[self.n_rig - 1] == 1 and (self.n_rig == 1 or self.righe[self.n_rig - 2] == 0):
            # devo controllare che la riga più bassa abbia 1 solo elemento e che la penultima 0 (se c'è)
            # l'ultimo che ha giocato ha vinto
            return 'ultimo'
