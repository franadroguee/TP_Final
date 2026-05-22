import pygame
from mapa import mapa, renderizado
from personajes import pacman
from copy import deepcopy

graficos = {
    'pared': pygame.image.load('graficos\pared.png'),
    'pasillo': pygame.image.load('graficos\pasillo.png'),
    'power': pygame.image.load('graficos\powerpellet.png'),
    'puerta': pygame.image.load('graficos\puerta.png'),
    'punto': pygame.image.load('graficos\punto.png'),
    'tunel': pygame.image.load('graficos\gtunel.png')
    }

superficie_jugador = pygame.image.load('graficos\Pac_Man.png')

# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((560, 775))
playing = True
clock = pygame.time.Clock()
jugador = pacman(20, 20, 1)
dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  

def rotar_imagen(jugador):
    if jugador.direccion == 'right':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 0)
    elif jugador.direccion == 'left':
        superficie_jugador_r = pygame.transform.flip(superficie_jugador, True, False)
    elif jugador.direccion == 'up':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 90)
    elif jugador.direccion == 'down':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 270)
        
    return superficie_jugador_r


# loop del juego
while playing:
    pantalla.fill((0, 0, 0))
    renderizado(pantalla, dic_mapa, graficos)
    snapshot = deepcopy(dic_mapa)
    dic_mapa = jugador.frame(snapshot)
    superficie_jugador_r = rotar_imagen(jugador)
    pantalla.blit(superficie_jugador_r, (jugador.posx, jugador.posy))
    pygame.display.update()
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
    clock.tick(60)
           
    
