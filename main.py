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
superficie_jugador_cerrado = pygame.image.load('graficos\Pac_Man_Cerrado.png')

# inicializacion de pygame
pygame.init()
pantalla = pygame.display.set_mode((560, 775))
playing = True
clock = pygame.time.Clock()
dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  
for numero, casilla in dic_mapa.items():
    if casilla == 'inicio':
        x_inicial, y_inicial = numero
        break
jugador = pacman(x_inicial * 20, y_inicial * 20, 5)

def rotar_imagen(jugador):
    if jugador.direccion == 'right':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 0)
        superficie_jugador_cerrado_r = pygame.transform.rotate(superficie_jugador_cerrado, 0)
    elif jugador.direccion == 'left':
        superficie_jugador_r = pygame.transform.flip(superficie_jugador, True, False)
        superficie_jugador_cerrado_r = pygame.transform.flip(superficie_jugador_cerrado, True, False)
    elif jugador.direccion == 'up':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 90)
        superficie_jugador_cerrado_r = pygame.transform.rotate(superficie_jugador_cerrado, 90)
    elif jugador.direccion == 'down':
        superficie_jugador_r = pygame.transform.rotate(superficie_jugador, 270)
        superficie_jugador_cerrado_r = pygame.transform.rotate(superficie_jugador_cerrado, 270)
        
    return superficie_jugador_r, superficie_jugador_cerrado_r
recargar_grafico = pygame.image.load('graficos\GAME_OVER.png')
frame = 0
salto = 5 # cada {salto} frames, abre/ cierra la boca

# loop del juego
while playing:
    pantalla.fill((0, 0, 0))
    renderizado(pantalla, dic_mapa, graficos)
    snapshot = deepcopy(dic_mapa)
    dic_mapa = jugador.frame(snapshot)

    abnierto, cerrado = rotar_imagen(jugador)
    if frame < salto:
        pantalla.blit(abnierto, (jugador.posx, jugador.posy))
    elif frame < salto * 2:
        pantalla.blit(cerrado, (jugador.posx, jugador.posy))
    elif frame == salto * 2:
        pantalla.blit(recargar_grafico, (jugador.posx -40, jugador.posy-40))
        frame = 0
        
    pygame.display.update()
    
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                jugador.recepcion_input('up')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                jugador.recepcion_input('down')
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                jugador.recepcion_input('right')
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                jugador.recepcion_input('left')
    clock.tick(10)
    frame += 1
    
