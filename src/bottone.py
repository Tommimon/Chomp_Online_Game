import pygame as pg

BIANCO = (0, 0, 0)


class Bottone:
    def __init__(self, text, pos, dim, colore=BIANCO, bold=False):
        self.text = text
        self.colore = colore
        self.bold = bold
        self.rect = pg.Rect(pos, dim)
