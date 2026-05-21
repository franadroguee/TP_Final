import pygame
from mapa import mapa
from entidades import pacman

# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((560, 775))
playing = True
clock = pygame.time.Clock()



# loop del juego
while playing:
    dic_mapa = mapa('mapa.txt', pantalla)  
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
            elif event.key == pygame.K_RIGHT:
                pass
            elif event.key == pygame.K_LEFT:
                pass
           
    
