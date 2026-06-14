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

with open("high_score.txt") as f:
    highest_score = f.read().strip()
img = pygame.image.load("level.png" )
img = pygame.transform.scale(img, (614.4, 409.6))
def level(nivel, your_score):
    n=3
    while True:


        fuente_titulo = pygame.font.Font('PacMan_font.ttf', 100)
        fuente_chica =pygame.font.Font('PacMan_font.ttf', 30)
        fuente_mas_chica = pygame.font.Font('PacMan_font.ttf', 20)
        fuente_mini = pygame.font.Font('PacMan_font.ttf', 15)
        pantalla.blit(fondo, (0, 0))


        texto = fuente_mas_chica.render("Nivel "+ str(nivel)+" completado!", True, red)
        rect_texto = texto.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(texto, (rect_texto.x, 60))

        tu_score = fuente_chica.render("Tu puntaje", True, blanco)
        rect_texto_tu_score = tu_score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(tu_score, (rect_texto_tu_score.x, 150))

        score = fuente_chica.render(str(your_score), True, blanco)
        rect_texto_score = score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(score, (rect_texto_score.x, 200))

        press_enter = fuente_titulo.render(str(n), True, amarillo)
        rect_press_enter = press_enter.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(press_enter, (rect_press_enter.x, 570))

        rect_logo = img.get_rect(center=(280, 400))
        pantalla.blit(img, rect_logo)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        n -=1
        time.sleep(1)
        if n <= 0:
            return
    pygame.quit()

