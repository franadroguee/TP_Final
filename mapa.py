import pygame

def mapa(pantalla, ruta_archivo: str) -> dict:
    '''
    Recibe la ruta del archivo del mapa y lo analiza. Segun corresponda, inserta en la ventana de PyGame, el .png del grafico que corresponda y ademas devuelve un diccionario con la informacion de todo el mapa en formato key=(x, y) value=str.
    
    args:
        ruta_archivo
    returns:
        dict
    '''
    
    # graficos
    pared = pygame.image.load('graficos\pared.png')
    pasillo = pygame.image.load('graficos\pasillo.png')
    power = pygame.image.load('graficos\powerpellet.png')
    puerta = pygame.image.load('graficos\puerta.png')
    punto = pygame.image.load('graficos\punto.png')
    tunel = pygame.image.load('graficos\gtunel.png')
    
    x = 0
    y = 3
    dic_mapa = {}
    with open(ruta_archivo, 'r') as mapa:
        for fila in mapa:
            for letra in fila:
                if letra == 'X': # pared
                    pantalla.blit(pared, ((x * 20), (y * 20))) # carga el grafico
                    dic_mapa[(x, y)] = 'pared' # adjunta la pos. al diccionario
                elif letra == '.': # punto
                    pantalla.blit(punto, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'punto'
                elif letra == ' ': # pasillo
                    pantalla.blit(pasillo, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'pasillo'
                elif letra == 'G': # Ghost house
                    pantalla.blit(pasillo, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'ghost'
                elif letra == 'o': # PowerPellet
                    pantalla.blit(power, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'powerpellet'
                elif letra == '-': # puerta ghost house
                    pantalla.blit(puerta, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'puerta'
                elif letra == 'T': # tunel lateral
                    pantalla.blit(tunel, ((x * 20), (y * 20)))
                    dic_mapa[(x, y)] = 'tunel'
                elif letra == 'P':
                    dic_mapa[(x, y)] = 'inicio'
                x += 1
            x = 0
            y += 1
    pygame.display.update()
    return dic_mapa

def renderizado(pantalla, dic_mapa: dict) -> None:
    '''
    Recibe la ruta del archivo del mapa y lo analiza. Segun corresponda, inserta en la ventana de PyGame, el .png del grafico que corresponda y ademas devuelve un diccionario con la informacion de todo el mapa en formato key=(x, y) value=str.
    
    args:
        ruta_archivo
    returns:
        dict
    '''
    
    # graficos
    pared = pygame.image.load('graficos\pared.png')
    pasillo = pygame.image.load('graficos\pasillo.png')
    power = pygame.image.load('graficos\powerpellet.png')
    puerta = pygame.image.load('graficos\puerta.png')
    punto = pygame.image.load('graficos\punto.png')
    tunel = pygame.image.load('graficos\gtunel.png')
    
    x = 0
    y = 3

    for elemento in dic_mapa.items():
        
        numero, celda = elemento
        if numero[0] == 0:
            x = 0
            y += 1

        if celda == 'X': # pared
            pantalla.blit(pared, ((x * 20), (y * 20))) # carga el grafico
            dic_mapa[(x, y)] = 'pared' # adjunta la pos. al diccionario
        elif celda == '.': # punto
            pantalla.blit(punto, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'punto'
        elif celda == ' ': # pasillo
            pantalla.blit(pasillo, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'pasillo'
        elif celda == 'G': # Ghost house
            pantalla.blit(pasillo, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'ghost'
        elif celda == 'o': # PowerPellet
            pantalla.blit(power, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'powerpellet'
        elif celda == '-': # puerta ghost house
            pantalla.blit(puerta, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'puerta'
        elif celda == 'T': # tunel lateral
            pantalla.blit(tunel, ((x * 20), (y * 20)))
            dic_mapa[(x, y)] = 'tunel'
        elif celda == 'P':
            dic_mapa[(x, y)] = 'inicio'
        x += 1

