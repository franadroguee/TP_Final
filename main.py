import pygame
from mapa import mapa, renderizado
from personajes import pacman, fantasma
from copy import deepcopy

pygame.init()
pantalla = pygame.display.set_mode((560, 775))

graficos = {
    'pared': pygame.image.load('graficos\Pac_Man.png'),
    'pasillo': pygame.image.load('graficos\seisiete.png'),
    'power': pygame.image.load('graficos\Background.png'),
    'puerta': pygame.image.load('graficos\Background.png'),
    'punto': pygame.image.load('graficos\Background.png'),
    'tunel': pygame.image.load('graficos\seisiete.png')
    }

superficie_jugador = pygame.image.load('graficos\GAME_OVER.png')
superficie_jugador_cerrado = pygame.image.load('graficos\GAME_OVER.png')

superficie_fantasma = pygame.image.load('graficos\powerpellet.png')

game_font = pygame.font.Font(None, 50)
white = (255, 255, 255)

# inicializacion de pygame
playing = True
clock = pygame.time.Clock()
dic_mapa = mapa(pantalla, 'mapa.txt', graficos)  
for numero, casilla in dic_mapa.items():
    if casilla == 'inicio':
        x_inicial, y_inicial = numero
        break
    
velocidad = 60 # casillas / segundo
v_final = velocidad * 20 / 60
jugador = pacman(x_inicial * 20, y_inicial * 20, round(v_final, 2))
info_bots = ((x_inicial, y_inicial), jugador.direccion)

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

blinky = fantasma(20, 20, v_final, 'blinky')

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
        info_bots = ((jugador.posx, jugador.posy), jugador.direccion)
        
    blinky.frame_ghost(dic_mapa, info_bots)
    
    pantalla.blit(text_surface, (100, 620))

    abnierto, cerrado = rotar_imagen(jugador)
    if frame < salto:
        pantalla.blit(abnierto, (jugador.posx - 40, jugador.posy- 40))
    elif frame < salto * 2:
        pantalla.blit(cerrado, (jugador.posx- 40, jugador.posy- 40))
    elif frame == salto * 2:
        pantalla.blit(cerrado, (jugador.posx- 40, jugador.posy- 40))        
        frame = 0
        
    pantalla.blit(superficie_fantasma, (blinky.posx, blinky.posy))
        
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
    clock.tick(60)
    frame += 1
    contador += 1
    
