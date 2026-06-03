from math import sqrt

def calcular_distancias(pos1: tuple, pos2: tuple) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    
    dist_X = abs(x2 - x1)
    dist_y = abs(y2 - y1)
    
    return sqrt(dist_X**2 + dist_y**2)

def pinky(x: int, y: int, info_pacman: tuple, mapa: dict) -> str:
    """
    Recibe la posicion del fantasma cuando este esta centrado en una casilla y devuelve un string con la direccion que debe tomar para dirigirse a su casilla de destino.
    """
    
    pac_pos, pas_dir = info_pacman
    pac_x, pac_y = info_pacman
    
    