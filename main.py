import pygame
from mapa import mapa, renderizado
from personajes import pacman

graficos = {
    'pared': pygame.image.load('graficos\pared.png'),
    'pasillo': pygame.image.load('graficos\pasillo.png'),
    'power': pygame.image.load('graficos\powerpellet.png'),
    'puerta': pygame.image.load('graficos\puerta.png'),
    'punto': pygame.image.load('graficos\punto.png'),
    'tunel': pygame.image.load('graficos\gtunel.png')
    }


# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((560, 775))
playing = True
clock = pygame.time.Clock()
jugador = pacman(20, 20, 1)

dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  

# loop del juego
while playing:
    pantalla.fill((0, 0, 0))
    renderizado(pantalla, dic_mapa, graficos)
    jugador.frame(dic_mapa)
    pygame.draw.circle(pantalla, (255, 255, 255), ((jugador.posx +10), (jugador.posy +10)), 10)
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
           
    
