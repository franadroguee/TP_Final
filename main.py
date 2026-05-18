import pygame
from mapa import mapa

# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((700, 775))
playing = True
clock = pygame.time.Clock()

# loop del juego
while playing:
    dic_mapa = mapa('mapa.txt', pantalla)  
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
