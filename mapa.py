import pygame

pygame.init()
pantalla = pygame.display.set_mode((930, 840))
playing = True
clock = pygame.time.Clock()

# graficos
pared = pygame.image.load('graficos\pared.png')
pasillo = pygame.image.load('graficos\pasillo.png')
power = pygame.image.load('graficos\powerpellet.png')
puerta = pygame.image.load('graficos\puerta.png')
punto = pygame.image.load('graficos\punto.png')


def mapa(ruta_archivo: str) -> dict:
    x = 0
    y = 0
    dic_mapa = {}
    with open(ruta_archivo, 'r') as mapa:
        for fila in mapa:
            for letra in fila:
                if letra == 'X':
                    pantalla.blit(pared, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'pared'
                elif letra == '.':
                    pantalla.blit(punto, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'punto'
                elif letra == ' ':
                    pantalla.blit(pasillo, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'pasillo'
                elif letra == 'G':
                    pantalla.blit(pasillo, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'ghost'
                elif letra == 'o':
                    pantalla.blit(power, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'powerpellet'
                elif letra == '-':
                    pantalla.blit(puerta, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'puerta'
                elif letra == 'T':
                    pantalla.blit(puerta, ((x * 30), (y * 30)))
                    dic_mapa[(x, y)] = 'tunel'
                elif letra == 'P':
                    dic_mapa[(x, y)] = 'inicio'
                x += 1
            x = 0
            y += 1
    pygame.display.update()
    return dic_mapa

while playing:
    dic_mapa = mapa('mapa.txt')  
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            playing = False
