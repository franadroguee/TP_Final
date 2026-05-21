import pygame
from mapa import mapa, renderizado
from entidades import pacman

# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((560, 775))
playing = True
clock = pygame.time.Clock()
jugador = pacman(200, 200, 5)

dic_mapa = mapa(pantalla, 'mapa.txt')  

# loop del juego
while playing:
    renderizado(pantalla, dic_mapa)
    grafico_jugador = pygame.draw.circle(pantalla, (255, 255, 255), ((jugador.posx -10), (jugador.posy -10)), 10)
    jugador.movimeinto()
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jugador.recepcion_input('up')
            elif event.key == pygame.K_DOWN:
                jugador.recepcion_input('down')
            elif event.key == pygame.K_RIGHT:
                jugador.recepcion_input('right')
            elif event.key == pygame.K_LEFT:
                jugador.recepcion_input('left')
           
    
