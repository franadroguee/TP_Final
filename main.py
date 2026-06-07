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
    'tunel': pygame.image.load(os.path.join(carpeta_graficos, 'pasillo.png')),
    'blinky': pygame.image.load(os.path.join(carpeta_graficos, 'blinky.png')),
    'pinky': pygame.image.load(os.path.join(carpeta_graficos, 'pinky.png'))
    }

superficie_jugador = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man.png'))
superficie_jugador_cerrado = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man_Cerrado.png'))

game_font = pygame.font.Font(None, 50)
white = (255, 255, 255)

# inicializacion de pygame
playing = True
clock = pygame.time.Clock()
dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  
ghost_spawn = []
ghost_places = []

# lectura casilla de inicio y ghost house
for numero, casilla in dic_mapa.items():
    if casilla == 'inicio':
        casilla_de_inicio = numero
    elif casilla == 'ghost':
        ghost_spawn.append(numero)
        ghost_places.append(numero)
    if casilla == 'puerta':
        ghost_places.append(numero)
    
# jugador
velocidad = 7.5 # casillas / segundo
v_final = velocidad * 20 / 60
pac_x_inic, pac_y_inic = casilla_de_inicio
jugador = pacman(pac_x_inic * 20, pac_y_inic * 20, round(v_final, 2))
pacman_rect = pygame.Rect(jugador.posx, jugador.posy, 20, 20)

# creacion de los fantasmas

nombres_fantasmas = ['pinky', 'pinky', 'pinky', 'pinky']

for i in range(4):
    bx, by = random.choice(ghost_spawn)
    spawn = (bx, by)

bx, by = random.choice(ghost_spawn)
spawn = (bx, by)
fantasma1 = fantasma(bx*20, by*20, v_final, 'blinky', spawn)
fantasma1_rect = pygame.Rect(bx*20, by*20, 20, 20)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
spawn = (bx, by)
fantasma2 = fantasma(bx*20, by*20, v_final, 'blinky', spawn)
fantasma2_rect = pygame.Rect(bx*20, by*20, 20, 20)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
spawn = (bx, by)
fantasma3 = fantasma(bx*20, by*20, v_final, 'pinky', spawn)
fantasma3_rect = pygame.Rect(bx*20, by*20, 20, 20)
ghost_spawn.remove((bx, by))

bx, by = random.choice(ghost_spawn)
spawn = (bx, by)
fantasma4 = fantasma(bx*20, by*20, v_final, 'pinky', spawn)
fantasma4_rect = pygame.Rect(bx*20, by*20, 20, 20)
ghost_spawn.remove((bx, by))

fantasmas = [fantasma1, fantasma2, fantasma3, fantasma4]
fantasmas_rect = [fantasma1_rect, fantasma2_rect, fantasma3_rect, fantasma4_rect]

def rotar_imagen(jugador):
    transformaciones = {
        'right': lambda imagen: pygame.transform.rotate(imagen, 0),
        'left':  lambda imagen: pygame.transform.flip(imagen, True, False),
        'up':    lambda imagen: pygame.transform.rotate(imagen, 90),
        'down':  lambda imagen: pygame.transform.rotate(imagen, 270),
    }
    
    t = transformaciones[jugador.direccion]
    return t(superficie_jugador), t(superficie_jugador_cerrado)        

salto = 0.2 # cada {salto} segundos, abre/ cierra la boca


puntaje = 0
vidas = 100
ultimo_chequeo_puntos = 0

# loop del juego
while playing:
    segundos = pygame.time.get_ticks()/1000
    text_surface = game_font.render(f"Puntaje: {puntaje} pts. Vidas: {vidas}", True, white)
        
    pantalla.fill((0, 0, 0))
    if segundos - ultimo_chequeo_puntos >= 3:
        hay_puntos = False
        for item in dic_mapa.values():
            if item == 'punto' or item == 'power':
                hay_puntos = True
                break
            
        if hay_puntos:
            pass
        else:
            dic_mapa = mapa(pantalla, 'mapa.txt', graficos)
            jugador.posx = pac_x_inic * 20
            jugador.posy = pac_y_inic * 20
                
        ultimo_chequeo_puntos = segundos
        
    # Renderizado
    renderizado(pantalla, dic_mapa, graficos)
    dic_mapa, puntaje, comio_powerpellet = jugador.frame_pacman(dic_mapa, puntaje)
         
    if comio_powerpellet:
        for ghost in fantasmas:
            ghost.cambio_de_modo('scared')     
                   
    info_bots = (jugador.casilla, jugador.direccion)        
    
    for ghost, rect in zip(fantasmas, fantasmas_rect):
        ghost.frame_ghost(ghost_places, dic_mapa, info_bots, graficos[ghost.nombre], pantalla)
        rect.topleft = (ghost.posx, ghost.posy)
    
    pantalla.blit(text_surface, (100, 620))

    abnierto, cerrado = rotar_imagen(jugador)
    
    fase = (segundos // salto) % 2
    if fase == 0 :
        pantalla.blit(abnierto, (jugador.posx, jugador.posy))
    else:
        pantalla.blit(cerrado, (jugador.posx, jugador.posy))
    
    pacman_rect.topleft = (jugador.posx, jugador.posy)

    pygame.display.update()
    
    for ghost, rect in zip(fantasmas, fantasmas_rect):
        if pacman_rect.colliderect(rect):
            vidas -= 1
            for numero, casilla in dic_mapa.items():
                if casilla == 'inicio':
                    x_inicial, y_inicial = numero
                    jugador.posx = x_inicial * 20
                    jugador.posy = y_inicial * 20
                    break
                
            for ghost in fantasmas:
                ghost.posx = ghost.spawn[0] * 20
                ghost.posy = ghost.spawn[1] * 20
                ghost.salio_house = False

        
    if vidas == 0:
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

