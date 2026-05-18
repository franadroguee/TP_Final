import pygame

pygame.init()
pantalla = pygame.display.set_mode((930, 840))
playing = True
clock = pygame.time.Clock()

pared = pygame.image.load('graficos\pared.png')
pasillo = pygame.image.load('graficos\pasillo.png')
power = pygame.image.load('graficos\powerpellet.png')
puerta = pygame.image.load('graficos\puerta.png')
punto = pygame.image.load('graficos\punto.png')

while playing:
    x = 0
    y = 0
    with open('mapa.txt', 'r') as mapa:
        for fila in mapa:
            for letra in fila:
                if letra == 'X':
                    pantalla.blit(pared, (x, y))
                elif letra == '.':
                    pantalla.blit(punto, (x, y))
                elif letra == ' ':
                    pantalla.blit(pasillo, (x, y))
                elif letra == 'G':
                    pantalla.blit(pasillo, (x, y))
                elif letra == 'o':
                    pantalla.blit(power, (x, y))
                elif letra == '-':
                    pantalla.blit(puerta, (x, y))
                elif letra == 'T':
                    pantalla.blit(puerta, (x, y))
                x += 30
            x = 0
            y += 30
    pygame.display.update()
            
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
