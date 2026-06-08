import pygame
import os
from mapa import mapa, renderizado
from personajes import pacman, fantasma
import random

pygame.init()
pantalla = pygame.display.set_mode((560, 775))
carpeta_graficos = 'graficos'

fases = [
    ("scatter", 7),
    ("chase",   20),
    ("scatter", 7),
    ("chase",   20),
    ("scatter", 5),
    ("chase",   20),
    ("scatter", 5),
    ("chase",   None),
]

def fase_actual(tiempo):
    for modo, duracion_modo in fases:
        if duracion_modo == None:
            return modo
        elif tiempo < duracion_modo:
            return modo
        else: 
            tiempo -= duracion_modo

graficos = {
    'pared': pygame.image.load(os.path.join(carpeta_graficos, 'pared.png')),
    'pasillo': pygame.image.load(os.path.join(carpeta_graficos, 'pasillo.png')),
    'power': pygame.image.load(os.path.join(carpeta_graficos, 'powerpellet.png')),
    'puerta': pygame.image.load(os.path.join(carpeta_graficos, 'puerta.png')),
    'punto': pygame.image.load(os.path.join(carpeta_graficos, 'punto.png')),
    'tunel': pygame.image.load(os.path.join(carpeta_graficos, 'pasillo.png')),
    'blinky': pygame.image.load(os.path.join(carpeta_graficos, 'blinky.png')),
    'inky': pygame.image.load(os.path.join(carpeta_graficos, 'inky.png')),
    'clyde': pygame.image.load(os.path.join(carpeta_graficos, 'clyde.png')), 
    'pinky': pygame.image.load(os.path.join(carpeta_graficos, 'pinky.png')), 
    'scared': pygame.image.load(os.path.join(carpeta_graficos, 'scared_ghost.png')),
    'volver_a_casa': pygame.image.load(os.path.join(carpeta_graficos, 'volver_a_casa.png'))
    }

superficie_jugador = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man.png'))
superficie_jugador_cerrado = pygame.image.load(os.path.join(carpeta_graficos, 'Pac_Man_Cerrado.png'))

game_font = pygame.font.Font(None, 50)
white = (255, 255, 255)

# inicializacion de pygame
playing = True
clock = pygame.time.Clock()
dic_mapa = mapa('mapa.txt', graficos)  
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
    
# velocidades -----------------------------------------------
velocidad_maxima = 7.5 # casillas / segundo
velocidad_aplicada = velocidad_maxima * 20 / 60
porcentaje_velocidad = lambda porcentaje: round((velocidad_aplicada * porcentaje / 100), 2)

pac_x_inic, pac_y_inic = casilla_de_inicio
jugador = pacman(pac_x_inic * 20, pac_y_inic * 20, porcentaje_velocidad(80))
pacman_rect = pygame.Rect(jugador.posx, jugador.posy, 20, 20)
vida_extra_otorgada = False
# creacion de los fantasmas

nombres_fantasmas = ['pinky', 'blinky', 'clyde', 'inky']
esquinas_fantasmas = [(0, 0), (28, 0), (0, 31), (28, 31)]
fantasmas = []
rects_fantasmas = []
posiciones_fantasmas = []


for i in range(4):
    start_x, start_y = random.choice(ghost_spawn)
    spawn = (start_x, start_y)
    f = fantasma(start_x * 20, start_y * 20, porcentaje_velocidad(75), nombres_fantasmas[i], spawn, esquinas_fantasmas[i])
    fantasmas.append(f)
    posiciones_fantasmas.append(f.casilla)
    rects_fantasmas.append(pygame.Rect(start_x * 20, start_y * 20, 20, 20))
    ghost_spawn.remove((start_x, start_y))
    
if 'blinky' in nombres_fantasmas:
    index = nombres_fantasmas.index('blinky')
else:
    index = random.randint(0, 3)
    
blinky_pos = posiciones_fantasmas[index]

def rotar_imagen_jugador(jugador):
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
vidas = 3

ultimo_chequeo_puntos = 0

ultimo_powerpellet_comido = 0
fantasmas_scared = False

modo_fantasmas_global = 'scatter'
tiempo_pausado = 0
inicio_fases = 0

cantidad_fantasmas_comidos = 0
puntaje_por_fantasmas_comidos = [0, 200, 400, 800, 1600]

# loop del juego
while playing:
    # si se superan los 10000 puntos, se otorga una vida extra una unica vez
    if puntaje >= 10000 and not vida_extra_otorgada:
        vidas += 1
    
    segundos = pygame.time.get_ticks()/1000 #tiempo de juego
    text_surface = game_font.render(f"Puntaje: {puntaje} pts. Vidas: {vidas}", True, white) # actualizacion puntaje
        
    # chequeo de puntos ----------------------------------------------------------------
    if segundos - ultimo_chequeo_puntos >= 3:
        hay_puntos = False
        for item in dic_mapa.values():
            if item == 'punto' or item == 'power':
                hay_puntos = True
                break
            
        if hay_puntos:
            pass
        else:
            dic_mapa = mapa('mapa.txt', graficos)
            jugador.posx = pac_x_inic * 20
            jugador.posy = pac_y_inic * 20
                
        ultimo_chequeo_puntos = segundos
 
    pantalla.fill((0, 0, 0))
        
    # Renderizado del mapa -----------------------------------------------------------------------------------
    renderizado(pantalla, dic_mapa, graficos)
    dic_mapa, puntaje, comio_powerpellet = jugador.frame_pacman(dic_mapa, puntaje)
         
    # efecto de los powerpellets ------------------------------------------------------------------
    if comio_powerpellet:
        if fantasmas_scared:
            tiempo_pausado += segundos - ultimo_powerpellet_comido # ataja el ocasional caso de que un powerpellet sea comido durante el efecto de otro
        jugador.velocidad = porcentaje_velocidad(90)
        ultimo_powerpellet_comido = segundos
        fantasmas_scared = True
        for ghost in fantasmas:
            if ghost.modo not in ['salir_de_casa', 'volver_a_casa']:
                ghost.cambio_de_modo('scared')
                ghost.velocidad = porcentaje_velocidad(50)
            
    if fantasmas_scared and segundos - ultimo_powerpellet_comido > 5:
        jugador.velocidad = porcentaje_velocidad(80)
        fantasmas_scared = False
        cantidad_fantasmas_comidos = 0
        tiempo_pausado += segundos - ultimo_powerpellet_comido
        for ghost in fantasmas:
            if ghost.modo == 'scared':
                ghost.cambio_de_modo(modo_fantasmas_global)
                ghost.velocidad = porcentaje_velocidad(75)
 
    if not fantasmas_scared:
        tiempo_de_fase = segundos - inicio_fases - tiempo_pausado
        nuevo_modo = fase_actual(tiempo_de_fase)
        if nuevo_modo != modo_fantasmas_global:
            modo_fantasmas_global = nuevo_modo
            for ghost in fantasmas:
                if ghost.modo in ('scatter', 'chase'):
                    ghost.cambio_de_modo(modo_fantasmas_global)

    info_bots = (jugador.casilla, jugador.direccion)        
    
    for f, rect in zip(fantasmas, rects_fantasmas):
        if f.modo in ['chase', 'scatter', 'salir_de_casa']:
            f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, graficos[f.nombre], pantalla, blinky_pos)
        elif f.modo == 'scared':
            f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, graficos['scared'], pantalla, blinky_pos)
        else:
            f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, graficos['volver_a_casa'], pantalla, blinky_pos)
            
        rect.topleft = (f.posx, f.posy)
    
    pantalla.blit(text_surface, (100, 620))

    abnierto, cerrado = rotar_imagen_jugador(jugador)
    
    fase = (segundos // salto) % 2
    if fase == 0 :
        pantalla.blit(abnierto, (jugador.posx, jugador.posy))
    else:
        pantalla.blit(cerrado, (jugador.posx, jugador.posy))
    
    pacman_rect.topleft = (jugador.posx, jugador.posy)

    pygame.display.update()
    
    #  Colisiones -----------------------------------------------------------------------
    for ghost, rect in zip(fantasmas, rects_fantasmas):
        if pacman_rect.colliderect(rect):
            if ghost.modo == 'scared':
                cantidad_fantasmas_comidos += 1
                puntaje += puntaje_por_fantasmas_comidos[cantidad_fantasmas_comidos]
                ghost.cambio_de_modo('volver_a_casa')
                ghost.velocidad = porcentaje_velocidad(150)
            elif ghost.modo == 'volver_a_casa':
                pass
            else:
                inicio_fases = segundos
                modo_fantasmas_global = 'scatter'
                tiempo_pausado = 0
                
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
                    ghost.modo = 'salir_de_casa'

    # GAME OVER ---------------------------------------------------------------------------
    if vidas == 0:
        playing = False
    
    # recepcion input ---------------------------------------------------------------------
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

