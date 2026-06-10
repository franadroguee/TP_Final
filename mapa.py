import pygame

def mapa(ruta_archivo: str, graficos: dict) -> dict:
    '''
    Recibe la ruta del archivo del mapa y lo analiza. Segun corresponda, inserta en la ventana de PyGame, el .png del grafico que corresponda y ademas devuelve un diccionario con la informacion de todo el mapa en formato key=(x, y) value=str.
    
    args:
        ruta_archivo
    returns:
        dict
    '''
    
    # graficos
    x = 0
    y = 0
    dic_mapa = {}
    with open(ruta_archivo, 'r') as mapa:
        for fila in mapa:
            for letra in fila:
                if letra == 'X': # pared
                    dic_mapa[(x, y)] = 'pared' # adjunta la pos. al diccionario
                elif letra == '.': # punto
                    dic_mapa[(x, y)] = 'punto'
                elif letra == ' ': # pasillo
                    dic_mapa[(x, y)] = 'pasillo'
                elif letra == 'G': # Ghost house
                    dic_mapa[(x, y)] = 'ghost'
                elif letra == 'o': # PowerPellet
                    dic_mapa[(x, y)] = 'power'
                elif letra == '-': # puerta ghost house
                    dic_mapa[(x, y)] = 'puerta'
                elif letra == 'T': # tunel lateral
                    dic_mapa[(x, y)] = 'tunel'
                elif letra == 'P':
                    dic_mapa[(x, y)] = 'inicio'
                x += 1
            x = 0
            y += 1
    pygame.display.update()
    return dic_mapa

def renderizado(pantalla, dic_mapa: dict, graficos: dict) -> None:
    '''
    Recibe la ruta del archivo del mapa y lo analiza. Segun corresponda, inserta en la ventana de PyGame, el .png del grafico que corresponda y ademas devuelve un diccionario con la informacion de todo el mapa en formato key=(x, y) value=str.
    
    args:
        ruta_archivo
    returns:
        dict
    '''
    
    # graficos
    
    for elemento in dic_mapa.items(): # analiza todas las casillas del mapa
        
        numero, celda = elemento
        x, y = numero
        
        x *= 20
        y *= 20
        
        numero = (x, y)
        if celda == 'pared': # pared
            pantalla.blit(graficos['pared'], (numero)) # carga el grafico
        elif celda == 'punto': # punto
            pantalla.blit(graficos['punto'], (numero))
        elif celda == 'pasillo': # pasillo
            pass
        elif celda == 'ghost': # Ghost house
            pass
        elif celda == 'power': # PowerPellet
            pantalla.blit(graficos['power'], (numero))
        elif celda == 'puerta': # puerta ghost house
            pantalla.blit(graficos['puerta'], (numero))
        elif celda == 'tunel': # tunel lateral
            pass
        elif celda == 'inicio':
            pass
            



