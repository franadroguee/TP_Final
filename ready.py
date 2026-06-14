import pygame
from juego import main
import time
pygame.init()
negro = (0, 0, 0)
red = (255,0,0)
blanco = (255,255,255)
amarillo= amarillo = (255, 255, 0)
pantalla = pygame.display.set_mode((560, 775))
fondo = pygame.image.load("fondo_menu.jpg")

def ready():
    n = 3
    fuente_titulo = pygame.font.Font('PacMan_font.ttf', 50)
    while n > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'

        pantalla.blit(fondo, (0, 0))

        tu_score = fuente_titulo.render("Ready?", True, red)
        rect_texto_tu_score = tu_score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(tu_score, (rect_texto_tu_score.x, 200))

        counter = fuente_titulo.render(str(n), True, blanco)
        text_counter = counter.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(counter, (text_counter))

        pygame.display.update()

        time.sleep(1)
        n -= 1
    



