
def leggi_prop(lista_prop):
    file = open('properties.txt', 'r')
    output = [''] * len(lista_prop)  # la facico già della lunghezza giusta
    for riga in file:
        riga = riga.split(' =')  # adesso riga è una lista che comprende nome del campo e valore del campo
        nome = riga[0]
        if nome in lista_prop:  # se la riga è quella cercata allora aggiungo il valore all'output
            val = riga[1].replace('\n', '')  # devo togliere il carattere di a capo
            val = val.replace(' ', '')  # togliere gli spazi è importante anche per togliere quello iniziale se c'è
            output[lista_prop.index(nome)] = val  # metto il valore nella posizione del nome del campo nell'input
    return output

