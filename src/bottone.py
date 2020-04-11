import pygame as pg

BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
FONT = 'freesansbold.ttf'


class Bottone:

    def __init__(self, text, pos, size=32, text_color=NERO, bg_color=BIANCO, bold=True):
        self.text = text
        self.pos = pos
        self.text_color = text_color
        self.bg_color = bg_color
        self.bold = bold
        self.font = pg.font.Font(FONT, size)
        self.rect = None

    def blit(self, screen):
        surface = self.font.render(self.text, self.bold, self.text_color, self.bg_color)
        self.rect = surface.get_rect()  # aggiorno il rect che identifica la parte cliccabile
        screen.blit(surface, self.pos)

    def ceck_click(self, mouse_pos):
        self.rect.topleft = self.pos
        return self.rect.collidepoint(mouse_pos)


