import pygame
import os
from mapa import mapa, renderizado
from personajes import pacman, fantasma
from copy import deepcopy
import random

pygame.init()
pantalla = pygame.display.set_mode((560, 775))
carpeta_graficos = 'graficos'

graficos = {
    'pared': pygame.image.load(os.path.join(carpeta_graficos, 'pared.png')),
    'pasillo': pygame.image.load(os.path.join(carpeta_graficos, 'pasillo.png')),
    'power': pygame.image.load(os.path.join(carpeta_graficos, 'powerpellet.png')),
    'puerta': pygame.image.load(os.path.join(carpeta_graficos, 'puerta.png')),
    'punto': pygame.image.load(os.path.join(carpeta_graficos, 'punto.png')),
    'tunel': pygame.image.load(os.path.join(carpeta_graficos, 'pasillo.png'))
    }

superficie_jugador = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man.png'))
superficie_jugador_cerrado = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man_Cerrado.png'))

superficie_fantasma = pygame.image.load(os.path.join(carpeta_graficos, 'Background.png'))

game_font = pygame.font.Font(None, 50)
white = (255, 255, 255)

# inicializacion de pygame
playing = True
clock = pygame.time.Clock()
dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  
ghost_spawn = []
ghost_places = []

for numero, casilla in dic_mapa.items():
    if casilla == 'inicio':
        x_inicial, y_inicial = numero
    elif casilla == 'ghost':
        ghost_spawn.append(numero)
        ghost_places.append(numero)
    if casilla == 'puerta':
        ghost_places.append(numero)
    

velocidad = 7.5 # casillas / segundo
v_final = velocidad * 20 / 60
jugador = pacman(x_inicial * 20, y_inicial * 20, round(v_final, 2))
pacman_rect = pygame.Rect(jugador.posx, jugador.posy, 20, 20)
info_bots = ((x_inicial, y_inicial), jugador.direccion)

bx, by = random.choice(ghost_spawn)
blinky = fantasma(bx*20, by*20, v_final, 'blinky')
blinky_rect = pygame.Rect(bx*20, by*20, 20, 20)
pos_b = (bx, by)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
blinky2 = fantasma(bx*20, by*20, v_final, 'blinky')
blinky2_rect = pygame.Rect(bx*20, by*20, 20, 20)
pos_b2 = (bx, by)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
blinky3 = fantasma(bx*20, by*20, v_final, 'blinky')
blinky3_rect = pygame.Rect(bx*20, by*20, 20, 20)
pos_b3 = (bx, by)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
blinky4 = fantasma(bx*20, by*20, v_final, 'blinky')
blinky4_rect = pygame.Rect(bx*20, by*20, 20, 20)
pos_b4 = (bx, by)
ghost_spawn.remove((bx, by))

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
contador = 0
salto = 30 # cada {salto} frames, abre/ cierra la boca


puntaje = 0

# loop del juego
while playing:
    
    text_surface = game_font.render(f"Puntaje: {puntaje} pts.", True, white)
        
    pantalla.fill((0, 0, 0))
    if contador == 180:
        hay_puntos = False
        for item in dic_mapa.values():
            if item == 'punto' or item == 'power':
                hay_puntos = True
                break
        if hay_puntos:
            pass
        else:
            dic_mapa = mapa(pantalla, 'mapa.txt', graficos)
            for numero, casilla in dic_mapa.items():
                if casilla == 'inicio':
                    x_inicial, y_inicial = numero
                    jugador.posx = x_inicial * 20
                    jugador.posy = y_inicial * 20
                    break

        contador = 0
        
    renderizado(pantalla, dic_mapa, graficos)
    snapshot = deepcopy(dic_mapa)
    dic_mapa, puntaje = jugador.frame_pacman(snapshot, puntaje)
    
    if jugador.posicion_perfecta():
        info_bots = ((jugador.posx/20, jugador.posy/20), jugador.direccion)
        
    render = blinky.ghost_render(ghost_places, dic_mapa, info_bots, superficie_fantasma, pantalla, pos_b)
    blinky_rect.topleft = (blinky.posx, blinky.posy)
    if render != None:
        pos_b = render
        
    render = blinky2.ghost_render(ghost_places, dic_mapa, info_bots, superficie_fantasma, pantalla, pos_b2)
    blinky2_rect.topleft = (blinky2.posx, blinky2.posy)
    if render != None:
        pos_b2 = render
        
    render = blinky3.ghost_render(ghost_places, dic_mapa, info_bots, superficie_fantasma, pantalla, pos_b3)
    blinky3_rect.topleft = (blinky3.posx, blinky3.posy)
    if render != None:
        pos_b3 = render
        
    render = blinky4.ghost_render(ghost_places, dic_mapa, info_bots, superficie_fantasma, pantalla, pos_b4)
    blinky4_rect.topleft = (blinky4.posx, blinky4.posy)
    if render != None:
        pos_b4 = render

    pantalla.blit(text_surface, (100, 620))

    abnierto, cerrado = rotar_imagen(jugador)
    if frame < salto:
        pantalla.blit(abnierto, (jugador.posx, jugador.posy))
    elif frame < salto * 2:
        pantalla.blit(cerrado, (jugador.posx, jugador.posy))
    elif frame == salto * 2:
        pantalla.blit(cerrado, (jugador.posx, jugador.posy))        
        frame = 0
    
    pacman_rect.topleft = (jugador.posx, jugador.posy)

    pygame.display.update()
    
    if pacman_rect.colliderect(blinky_rect) or pacman_rect.colliderect(blinky2_rect) or pacman_rect.colliderect(blinky3_rect) or pacman_rect.colliderect(blinky4_rect):
        playing = False
    
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
    clock.tick(60)
    frame += 1
    contador += 1
    
