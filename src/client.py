from src.tavola import *
succes, fail = pygame.init()
print("{0} successes and {1} failures".format(succes, fail))

# PARAMETRI
FPS = 60  # Frames per second.
RISOLUZIONE = (720, 480)
NERO = (0, 0, 0)
DIM_CAS = 64
PADDING = 4

screen = pygame.display.set_mode(RISOLUZIONE)  # mostro schermo
clock = pygame.time.Clock()  # inizializzo clock

tavoletta = Tavola(0, 0, 720, 480, 10, 20, PADDING)
print("kmffdlknsdsflkmdslkm")
tavoletta.disegna()

while True:
    clock.tick(FPS)  # mi fa andare al giusto frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tavoletta.ceck_click(event.pos)
        elif event.type == FINEPARTITA:
            print('fine, ha vinto il ' + event.win + ' giocatore')

    screen.fill(NERO)
    tavoletta.blit(screen)
    pygame.display.update()  # Or pygame.display.flip()
