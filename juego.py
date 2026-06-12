def main():

    import pygame
    import os
    from mapa import mapa, renderizado
    from personajes import pacman, fantasma
    import random
    from menu import start
    from game_over import game_over


    # inicializacion de pygame -----------------------------------------------------------
    # pre_init con buffer chico = menos latencia al reproducir efectos (debe ir ANTES de pygame.init)
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.mixer.init()

    pantalla = pygame.display.set_mode((560, 775))

    cancion_base = pygame.mixer.music.load(os.path.join('sonidos-pacman', 'cancion-base.mp3'))
    sonido_muerte = pygame.mixer.Sound(os.path.join('sonidos-pacman', 'muerte.mp3'))
    sonido_comer_fantasma = pygame.mixer.Sound(os.path.join('sonidos-pacman', 'se-come-fantasma.mp3'))
    sonido_vida_extra = pygame.mixer.Sound(os.path.join('sonidos-pacman', 'vida-extra.mp3'))
    waka_waka = pygame.mixer.Sound(os.path.join('sonidos-pacman', 'pacman-waka-waka.wav'))  # WAV = sin delay del mp3

    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    fantasmas_y_esquinas = start()

    # modos globales --------------------------------------------------------------------------------------
    fases = [
        ("scatter", 7),
        ("chase", 20),
        ("scatter", 7),
        ("chase", 20),
        ("scatter", 5),
        ("chase", 20),
        ("scatter", 5),
        ("chase", None),
    ]


    def fase_actual(tiempo):
        """
        Devuelve un str con la fase actual, dependiendo de cuanto tiempo haya corrido el juego
        """

        for modo, duracion_modo in fases:
            if duracion_modo == None:  # chase infinito
                return modo
            elif tiempo < duracion_modo:
                # si el tiempo es menor a la duracion del modo, el modo global es ese.
                return modo
            else:
                tiempo -= duracion_modo  # si no, se le resta el tiempo de ese modo y se intenta denuevo


    # sprites ---------------------------------------------------------------------------------------
    graficos_mapa = {
        'pared': pygame.image.load(os.path.join('Sprites', 'pared.png')),
        'power': pygame.image.load(os.path.join('Sprites', 'powerpellet.png')),
        'puerta': pygame.image.load(os.path.join('Sprites', 'puerta.png')),
        'punto': pygame.image.load(os.path.join('Sprites', 'punto.png')),
        'tunel': pygame.image.load(os.path.join('Sprites', 'tunel.png')),
    }


    # Sprites --------------------------------------------------------------------------------------------
    def sprite_fantasma(fantasma, fase_sprites):
        if fantasma.modo == 'volver_a_casa':
            archivo = f'volver_a_casa_{fantasma.direccion}.png'
            return pygame.image.load(os.path.join('Sprites', archivo))

        if fantasma.nombre == "sleepy" and fantasma.modo == "sleep":
            archivo = f'sleepy_closed_{fantasma.direccion}.png'
            return pygame.image.load(os.path.join('Sprites', fase_sprites, archivo))

        nombre = fantasma.nombre
        direccion = fantasma.direccion

        archivo = f'{nombre}_{direccion}.png'
        return pygame.image.load(os.path.join('Sprites', fase_sprites, archivo))


    def sprite_pacman(jugador, fase_sprites):
        imagen = pygame.image.load(os.path.join('Sprites', fase_sprites, 'Pac_Man.png'))

        transformaciones = {
            'right': lambda imagen: pygame.transform.rotate(imagen, 0),
            'left': lambda imagen: pygame.transform.flip(imagen, True, False),
            'up': lambda imagen: pygame.transform.rotate(imagen, 90),
            'down': lambda imagen: pygame.transform.rotate(imagen, 270),
            None: lambda imagen: pygame.transform.rotate(imagen, 0)
        }

        t = transformaciones[jugador.direccion]
        return t(imagen)


    salto = 0.2  # cada {salto} se mueven las aletas de los fantasmas y PacMan abre/cierra la boca

    game_font = pygame.font.Font('PacMan_font.ttf', 25)
    white = (255, 255, 255)

    # inicio de la logica del juego ------------------------------------------------------------------
    playing = True
    clock = pygame.time.Clock()
    dic_mapa = mapa('mapa.txt', graficos_mapa)
    ghost_spawn = []
    ghost_places = []

    # lectura casilla de inicio y ghost house -----------------------------------------------------------
    for numero, casilla in dic_mapa.items():
        if casilla == 'inicio':
            casilla_de_inicio = numero
        elif casilla == 'ghost':
            ghost_spawn.append(numero)
            ghost_places.append(numero)
        if casilla == 'puerta':
            ghost_places.append(numero)

    # velocidades -----------------------------------------------
    velocidad_maxima = 7.5  # casillas / segundo
    velocidad_aplicada = velocidad_maxima * 20 / 60
    porcentaje_velocidad = lambda porcentaje: round((velocidad_aplicada * porcentaje / 100), 2)

    # inicializacion de pacman ---------------------------------------------------------
    pac_x_inic, pac_y_inic = casilla_de_inicio
    jugador = pacman(pac_x_inic * 20, pac_y_inic * 20, porcentaje_velocidad(80))
    pacman_rect = pygame.Rect(jugador.posx, jugador.posy, 20, 20)
    vida_extra_otorgada = False

    # inicializacion de los fantasmas ------------------------------------------------------------
    nombres_fantasmas = []
    esquinas_fantasmas = []
    for nombre, esquina in fantasmas_y_esquinas.items():
        nombres_fantasmas.append(nombre.lower())
        esquinas_fantasmas.append(esquina)

    fantasmas = []
    rects_fantasmas = []
    posiciones_fantasmas = []

    for i in range(4):
        start_x, start_y = random.choice(ghost_spawn)
        spawn = (start_x, start_y)
        f = fantasma(start_x * 20, start_y * 20, porcentaje_velocidad(75), nombres_fantasmas[i], spawn,
                     esquinas_fantasmas[i])
        fantasmas.append(f)
        posiciones_fantasmas.append(f.casilla)
        rects_fantasmas.append(pygame.Rect(start_x * 20, start_y * 20, 20, 20))
        ghost_spawn.remove((start_x, start_y))

    if 'blinky' in nombres_fantasmas:  # informacion de blinky para la logica de chase de inky
        indice_blinky = nombres_fantasmas.index('blinky')
    else:
        indice_blinky = random.randint(0, 3)

    # definicion de variables --------------------------------------------------------------------------------------
    fantasmas_activados = 0
    puntaje_final = 0

    puntaje = 0
    vidas = 3

    ultimo_chequeo_puntos = 0

    ultimo_powerpellet_comido = 0
    fantasmas_scared = False
    parpadeo_scared = False

    modo_fantasmas_global = 'scatter'
    tiempo_pausado = 0
    inicio_fases = 0

    cantidad_fantasmas_comidos = 0
    puntaje_por_fantasmas_comidos = [0, 200, 400, 800, 1600]

    fase_frame_anterior = 'fase1'

    tiempo_en_menu = pygame.time.get_ticks() / 1000
    # loop del juego --------------------------------------------------------------------------------------
    while playing:
        # si se superan los 10000 puntos, se otorga una vida extra una unica vez
        if puntaje >= 10000 and not vida_extra_otorgada:
            sonido_vida_extra.play()
            vidas += 1
            vida_extra_otorgada = True

        segundos = (pygame.time.get_ticks() / 1000) - tiempo_en_menu  # tiempo de juego
        text_surface1 = game_font.render(f"Puntaje: {puntaje} pts.", True, white)  # actualizacion puntaje
        text_surface2 = game_font.render(f"Vidas: {vidas}", True, white)

        # activacion de los fantasmas (salen en orden) --------------------------------------------------------------------------------------
        if fantasmas_activados < 1:
            fantasmas[0].modo = 'salir_de_casa'
            fantasmas_activados += 1
        elif (puntaje - puntaje_final) >= 30 and fantasmas_activados < 2:
            fantasmas[1].modo = 'salir_de_casa'
            fantasmas_activados += 1
        elif (puntaje - puntaje_final) >= 60 and fantasmas_activados < 3:
            fantasmas[2].modo = 'salir_de_casa'
            fantasmas_activados += 1
        elif (puntaje - puntaje_final) >= 90 and fantasmas_activados < 4:
            fantasmas[3].modo = 'salir_de_casa'
            fantasmas_activados += 1

        # LEVEL UP (revisa cada 3 segundos) ----------------------------------------------------------------
        if segundos - ultimo_chequeo_puntos >= 3:
            hay_puntos = False
            for item in dic_mapa.values():
                if item == 'punto' or item == 'power':
                    hay_puntos = True
                    break

            if hay_puntos:
                pass
            else:
                dic_mapa = mapa('mapa.txt', graficos_mapa)
                jugador.posx = pac_x_inic * 20
                jugador.posy = pac_y_inic * 20
                inicio_fases = segundos
                modo_fantasmas_global = 'scatter'
                tiempo_pausado = 0
                fantasmas_activados = 0
                puntaje_final = puntaje

                for ghost in fantasmas:
                    ghost.posx = ghost.spawn[0] * 20
                    ghost.posy = ghost.spawn[1] * 20
                    ghost.modo = None

            ultimo_chequeo_puntos = segundos

        pantalla.fill((0, 0, 0))  # elimina los sprites del frame anterior

        # Renderizado del mapa y logica PacMan -----------------------------------------------------------------------------------
        renderizado(pantalla, dic_mapa, graficos_mapa)
        dic_mapa, puntaje, comio_powerpellet = jugador.frame_pacman(dic_mapa, puntaje, waka_waka)

        # efecto de los powerpellets ------------------------------------------------------------------
        if comio_powerpellet:
            if fantasmas_scared:  # si comio un powerpellet durante el efecto de otro
                tiempo_pausado += segundos - ultimo_powerpellet_comido  # ataja el ocasional caso de que un powerpellet sea comido durante el efecto de otro
                parpadeo_scared = False

            jugador.velocidad = porcentaje_velocidad(90)  # pacman aumenta la velocidad
            ultimo_powerpellet_comido = segundos  # establece el timer

            fantasmas_scared = True

            for ghost in fantasmas:
                if ghost.modo not in ['salir_de_casa',
                                      'volver_a_casa']:  # en caso de que esten muertos o en el ghost house, su modo no se altera
                    ghost.cambio_de_modo('scared')
                    ghost.velocidad = porcentaje_velocidad(50)

        if fantasmas_scared and segundos - ultimo_powerpellet_comido > 4:  # comienzan a parpadear a los 4 segundos
            parpadeo_scared = True

            # fin del efecto del powerpellet --------------------------------------------------------------------------------------
        if fantasmas_scared and segundos - ultimo_powerpellet_comido > 6:
            parpadeo_scared = False
            jugador.velocidad = porcentaje_velocidad(80)  # pacman vuelve a su velocidad normal

            fantasmas_scared = False
            cantidad_fantasmas_comidos = 0  # se reinicia el multiplicador
            tiempo_pausado += segundos - ultimo_powerpellet_comido  # agrega el tiempo que el reloj estuvo pausado para las fases globales

            for ghost in fantasmas:
                if ghost.modo == 'scared':
                    ghost.cambio_de_modo(modo_fantasmas_global)
                    ghost.velocidad = porcentaje_velocidad(75)

        # manejo de los modos globales --------------------------------------------------------------------------------------
        if not fantasmas_scared:
            tiempo_de_fase = segundos - inicio_fases - tiempo_pausado
            nuevo_modo = fase_actual(tiempo_de_fase)

            if nuevo_modo != modo_fantasmas_global:  # cambio de modo global
                modo_fantasmas_global = nuevo_modo

                for ghost in fantasmas:
                    if ghost.modo in ('scatter', 'chase'):
                        ghost.cambio_de_modo(modo_fantasmas_global)

        info_bots = (jugador.casilla, jugador.direccion)

        # Fases de los Sprites ----------------------------------------------------------
        fase = (segundos // salto) % 2
        fase_sprites = 'fase1' if fase == 0 else 'fase2'

        fase_frame_anterior = fase_sprites

        # logica de los fantasmas --------------------------------------------------------------------------------------
        for f, rect in zip(fantasmas, rects_fantasmas):

            if f.modo in ['chase', 'scatter', 'salir_de_casa', None]:  # sprite normal
                imagen = sprite_fantasma(f, fase_sprites)
                f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, imagen, pantalla, fantasmas,
                              indice_blinky, segundos)

            elif f.modo == 'scared':
                if not parpadeo_scared:  # sprite 'scared'
                    imagen = pygame.image.load(os.path.join('Sprites', fase_sprites, 'scared.png'))
                else:  # si faltan 2 segundos o menos para que termine el efecto del parpadeo
                    imagen = pygame.image.load(os.path.join('Sprites', fase_sprites, 'scared.png')) if (
                                (segundos // 0.5) % 2 == 0) else pygame.image.load(
                        os.path.join('Sprites', fase_sprites, 'parpadeo_scared.png'))

                f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, imagen, pantalla, fantasmas,
                              indice_blinky, segundos)

            else:
                imagen = sprite_fantasma(f, fase_sprites)
                f.frame_ghost(porcentaje_velocidad(75), ghost_places, dic_mapa, info_bots, imagen, pantalla, fantasmas,
                              indice_blinky, segundos)

            rect.topleft = (f.posx, f.posy)

        # renderizado de PacMan -----------------------------------------------------------------------------
        pantalla.blit(text_surface1, (0, 630))  # puntaje y vidas
        pantalla.blit(text_surface2, (0, 670))

        pantalla.blit(sprite_pacman(jugador, fase_sprites), (jugador.posx, jugador.posy))

        pacman_rect.topleft = (jugador.posx, jugador.posy)

        pygame.display.update()

        #  Colisiones -----------------------------------------------------------------------
        for ghost, rect in zip(fantasmas, rects_fantasmas):
            if pacman_rect.colliderect(rect):
                if ghost.modo == 'scared':
                    sonido_comer_fantasma.play()
                    cantidad_fantasmas_comidos += 1
                    puntaje += puntaje_por_fantasmas_comidos[cantidad_fantasmas_comidos]
                    ghost.cambio_de_modo('volver_a_casa')
                    ghost.velocidad = porcentaje_velocidad(150)
                elif ghost.modo == 'volver_a_casa':
                    pass
                else:
                    sonido_muerte.play()
                    inicio_fases = segundos
                    modo_fantasmas_global = 'scatter'
                    tiempo_pausado = 0

                    vidas -= 1
                    jugador.posx = pac_x_inic * 20
                    jugador.posy = pac_y_inic * 20

                    for ghost in fantasmas:
                        ghost.posx = ghost.spawn[0] * 20
                        ghost.posy = ghost.spawn[1] * 20
                        ghost.modo = 'salir_de_casa'

        # GAME OVER ---------------------------------------------------------------------------
        if vidas == 0:
            playing = False
            with open("high_score.txt") as f:
                highest_score = f.read().strip()
            if puntaje > int(highest_score):
                with open("high_score.txt", "w") as f:
                    f.write(str(puntaje))
            game_over(puntaje)

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

