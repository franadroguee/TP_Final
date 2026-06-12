import pygame
import os
pygame.init()
fondo = pygame.image.load("fondo_menu.jpg")
# Cargamos todas las imagenes al principio y las de las carpetas
# para despues con un loop hacer la animacion, y el high score
pacman_logo = pygame.image.load("pacman-logo.png")
pacman_logo = pygame.transform.scale(pacman_logo, (424.2, 211.8))
gif_pacman = sorted(os.listdir("gif_pacman"))
frames_pacman = []
for n in gif_pacman:
    imagen = pygame.image.load(f"./gif_pacman/{n}")
    frames_pacman.append(imagen)

frames_coin = []
gif_coin = sorted(os.listdir("gif_coin"))
for n in gif_coin:
    imagen = pygame.image.load(f"./gif_coin/{n}")
    imagen = pygame.transform.scale(imagen, (50, 50))
    frames_coin.append(imagen)

with open("high_score.txt") as f:
    high_score = f.read().strip()

pantalla = pygame.display.set_mode((560, 775))

def crear_fantasma(name, color, desc, cords):
    return {"name": name, "color": color, "desc": desc, "cords": cords}


datos = [
    ("Blinky", "rojo",    "El perseguidor"),
    ("Pinky",  "rosa",    "El emboscador"),
    ("Inky",   "celeste", "El flanqueador"),
    ("Clyde",  "naranja", "El tímido"),
    ("Sleepy",  "gris",   "El dormido"),
    ("Coward", "violeta", "El cobarde"),
]

x, ancho, alto, espacio = 100, 360, 70, 15
y_inicial = 150

COLORES_RGB = {
    "rojo":    (255, 0, 0),
    "rosa":    (255, 105, 180),
    "celeste": (0, 200, 255),
    "naranja": (255, 140, 0),
    "gris":    (128, 128, 128),
    "violeta": (160, 32, 240),
}

fantasmas = []
for i, (name, color, desc) in enumerate(datos):
    y = y_inicial + i * (alto + espacio)
    fantasmas.append(crear_fantasma(name, color, desc, (x, y, ancho, alto)))

def pantalla_inicio(pantalla: pygame.Surface) -> bool:
    """Carga la pantalla inicial, inicia las animaciones devuelve true si el usuario presiona alguna key"""
    fuente_titulo = pygame.font.Font(None, 50)
    fuente_texto  = pygame.font.Font(None, 50)
    amarillo = (255, 221, 0)
    blanco   = (255, 255, 255)
    negro    = (0, 0, 0)

    reloj = pygame.time.Clock()

    while True:
        pantalla.blit(fondo, (0, 0))
        # titulo = fuente_titulo.render("PACMAN", True, amarillo)
        rect_logo = pacman_logo.get_rect(center=(280, 300))
        pantalla.blit(pacman_logo, rect_logo)
        #pantalla.blit(titulo, rect_titulo)
        indice_pacman = (pygame.time.get_ticks() // 50) % len(frames_pacman)
        pantalla.blit(frames_pacman[indice_pacman], (0, 0))
        texto_high = fuente_titulo.render("Highest Score:", True, blanco)
        rect_texto = texto_high.get_rect(center=(280, 400))
        rect_texto.y += 150
        pantalla.blit(texto_high, rect_texto)
        punto_high = fuente_titulo.render(high_score, True, blanco)
        rect_punto = punto_high.get_rect(center=(280, 400))
        rect_punto.y += 200
        pantalla.blit(punto_high, rect_punto)


        if (pygame.time.get_ticks() // 500) % 2 == 0:
            texto = fuente_texto.render("Insert Coin", True, COLORES_RGB["rojo"])
            rect_texto = texto.get_rect(center=(280, 400))
            pantalla.blit(texto, rect_texto)
            indice = (pygame.time.get_ticks() // 100) % len(frames_coin)
            frame = frames_coin[indice]
            rect_coin = frame.get_rect(midright=(rect_texto.left - 10, rect_texto.centery))
            pantalla.blit(frame, rect_coin)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True

        reloj.tick(60)

def menu_fantasmas(pantalla: pygame.Surface, fantasmas: list[dict]) -> list[dict]:

    """List -> List, obtiene la lista de diccionarios de todos los fantasmas y devuelve una lista de diccionarios con los fantasmas seleccionados"""
    fuente_titulo= pygame.font.Font(None, 40)
    fuente_grande = pygame.font.Font(None, 30)
    fuente_chica = pygame.font.Font(None, 20)
    blanco = (255, 255, 255)
    azul   = (33, 33, 222)
    amarillo = (255, 221, 0)
    negro = (0,0,0)
    fantasmas_seleccionados = []
    while True:
        pantalla.blit(fondo, (0, 0))
        texto = fuente_titulo.render("Eleji Los 4 Fantasmas", True, blanco)
        rect_texto = texto.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(texto, (rect_texto.x, 60))
        for f in fantasmas:
            rect = pygame.Rect(f["cords"])
            pygame.draw.rect(pantalla, negro, rect)
            if f in fantasmas_seleccionados:
                pygame.draw.rect(pantalla, amarillo, rect, 3)
            else:
                pygame.draw.rect(pantalla, blanco, rect, 3)

            texto = fuente_grande.render(f["name"], True, blanco)
            text_nombre = texto.get_rect(center=rect.center)
            text_nombre.y -= 13
            pantalla.blit(texto, text_nombre)
            texto_desc = fuente_chica.render(f["desc"], True, blanco)
            texto_desc_format = texto_desc.get_rect(center=rect.center)
            texto_desc_format.y += 10
            pantalla.blit(texto_desc, texto_desc_format)



            color_rgb = COLORES_RGB[f["color"]]
            centro = (rect.left + 30, rect.centery)
            pygame.draw.circle(pantalla, color_rgb, centro, 20)

        pygame.display.update()

        if len(fantasmas_seleccionados) >= 4:
            return fantasmas_seleccionados
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6:
                    indice = event.key - pygame.K_1
                    fantasma = fantasmas[indice]
                    fantasmas_seleccionados.append(fantasma)
            if event.type == pygame.QUIT:
                return

def menu_posiciones(pantalla: pygame.Surface, fantasmas_seleccionados: list[dict]) -> list[dict]:

    """List -> List, Toma los fantasmas seleccionados previament y les asigna una posicion a donde ir al comenzar el juego. Lo guarda en una lista con ficcionario de la forma: {fantasma}: {cordenadas}"""
    fuente_titulo = pygame.font.Font(None, 70)
    fuente_texto = pygame.font.Font(None, 30)
    fuente_texto_2 = pygame.font.Font(None, 50)
    negro = (0, 0, 0)
    blanco = (255, 255, 255)
    fantasmas_posiciones = {}
    sup_izq = (0,0)
    sup_der = (28,0)
    inf_izq = (0,31)
    inf_der = (28,31)
    posiciones = [sup_izq, sup_der, inf_izq, inf_der]
    def create_rec(n):
        n -= 1
        x, ancho, alto, y_inicial = 100, 360, 70, 150
        espacio = 100
        y = y_inicial + n*espacio
        return x, y, ancho, alto
    while True:
        if len(fantasmas_posiciones) >= 4:
            return fantasmas_posiciones
        for f in fantasmas_seleccionados:
            while f["name"] not in fantasmas_posiciones.keys():
                pantalla.blit(fondo, (0, 0))
                for pi, p in enumerate(posiciones):
                    if p == sup_izq:
                        text = "Superior Izquierda"
                        numb = "1"
                    if p == sup_der:
                        text = "Superior Derecha"
                        numb = "2"
                    if p == inf_izq:
                        text = "Inferior Izquierda"
                        numb = "3"
                    if p == inf_der:
                        text = "Inferior Derecha"
                        numb = "4"

                    if p not in fantasmas_posiciones.values():
                        rect = pygame.Rect(create_rec(pi+1))
                        pygame.draw.rect(pantalla, blanco, rect, 3)
                        texto = fuente_texto.render("Esquina "+text, True, blanco)
                        rect_texto = texto.get_rect(center=rect.center)

                        number = fuente_titulo.render(numb, True, blanco)
                        rect_num = number.get_rect(center=rect.center)
                        rect_num.x -= 230
                        pantalla.blit(texto, rect_texto)
                        pantalla.blit(number, rect_num)

                texto = fuente_texto_2.render(f'Eleji donde empieza {f["name"]}', True, COLORES_RGB[f["color"]])
                rect_texto = texto.get_rect(center=pantalla.get_rect().center)
                pantalla.blit(texto, (rect_texto.x, 60))
                pygame.display.update()


                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4:
                            if event.key == pygame.K_1 and sup_izq in posiciones:
                                fantasmas_posiciones[f["name"]] = sup_izq
                                posiciones.remove(sup_izq)
                            if event.key == pygame.K_2 and sup_der in posiciones:
                                fantasmas_posiciones[f["name"]] = sup_der
                                posiciones.remove(sup_der)
                            if event.key == pygame.K_3 and inf_izq in posiciones:
                                fantasmas_posiciones[f["name"]] = inf_izq
                                posiciones.remove(inf_izq)
                            if event.key == pygame.K_4 and inf_der in posiciones:
                                fantasmas_posiciones[f["name"]] = inf_der
                                posiciones.remove(inf_der)
                    if event.type == pygame.QUIT:
                            return


def start():
    seguir = pantalla_inicio(pantalla)
    if seguir:
        fantasmas_seleccionados = menu_fantasmas(pantalla, fantasmas)
        return menu_posiciones(pantalla, fantasmas_seleccionados)
    pygame.quit()
