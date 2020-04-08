# l'idea è che tutti conoscano questo modulo così  da poter chiamare Global.get('game') ad esempio
# questa classe conterrà in una var statica una lista di tutte le var globali
# le var statiche sono sccessibili ovunque se si importa la classe


class Globale:
    variabili_globali = []  # ogni variabile è un lista di nome e valore

    @staticmethod
    def new(nome, valore=None):
        Globale.variabili_globali.append([nome, valore])

    @staticmethod
    def set(nome, valore):
        for var in Globale.variabili_globali:
            if var[0] == nome:  # ver[0] è il nome
                var[1] = valore  # var[1] è il valore

    @staticmethod
    def get(nome):
        for var in Globale.variabili_globali:
            if var[0] == nome:  # ver[0] è il nome
                return var[1]  # var[1] è il valore
