import pygame
from juego import main
pygame.init()
negro = (0, 0, 0)
red = (255,0,0)
blanco = (255,255,255)
amarillo= amarillo = (255, 255, 0)
pantalla = pygame.display.set_mode((560, 775))
fondo = pygame.image.load("fondo_menu.jpg")

with open("high_score.txt") as f:
    highest_score = f.read().strip()
img = pygame.image.load("game_over.png" )
img = pygame.transform.scale(img, (614.4, 409.6))
def game_over(your_score):

    while True:


        fuente_titulo = pygame.font.Font('PacMan_font.ttf', 35)
        fuente_chica =pygame.font.Font('PacMan_font.ttf', 20)
        fuente_mini = pygame.font.Font('PacMan_font.ttf', 15)
        pantalla.blit(fondo, (0, 0))

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            texto = fuente_titulo.render("Game Over", True, red)
            rect_texto = texto.get_rect(center=pantalla.get_rect().center)
            pantalla.blit(texto, (rect_texto.x, 60))

        tu_score = fuente_chica.render("Tu puntaje", True, blanco)
        rect_texto_tu_score = tu_score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(tu_score, (rect_texto_tu_score.x, 150))

        score = fuente_chica.render(str(your_score), True, blanco)
        rect_texto_score = score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(score, (rect_texto_score.x, 200))

        max_score = fuente_chica.render("Highest Score", True, amarillo)
        rect_texto_max_score = max_score.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(max_score, (rect_texto_max_score.x, 260))

        max_score_puntos = fuente_chica.render(str(highest_score), True, amarillo)
        rect_texto_max_score_puntos = max_score_puntos.get_rect(center=pantalla.get_rect().center)
        pantalla.blit(max_score_puntos, (rect_texto_max_score_puntos.x, 310))
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            press_enter = fuente_mini.render("Toca una tecla", True, blanco)
            rect_press_enter = press_enter.get_rect(center=pantalla.get_rect().center)
            pantalla.blit(press_enter, (rect_press_enter.x, 650))

        rect_logo = img.get_rect(center=(270, 500))
        pantalla.blit(img, rect_logo)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main()
            elif event.type == pygame.QUIT:
                corriendo = False


    pygame.quit()

