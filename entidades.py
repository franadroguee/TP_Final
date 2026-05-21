class entidad:
    def __init__(self, posx, posy, velocidad):
        self.posx = posx
        self.posy = posy
        self.direccion = 'der' # 'right', 'left', 'up', 'down'
        self.direccion_deseada = 0
        self.velocidad = velocidad
    
    def cambiar_velocidad(self, nueva_velocidad: int):
        self.velocidad = nueva_velocidad
        
    def posicion_perfecta(self):
        if self.posx % 25 == 0 and self.posy % 25 == 0:
            return True
        else:
            return False
        
    def puede_moverse(self, mapa:dict) -> bool:
        x = self.posx / 25
        y = self.posy / 25
        
        if self.direccion == 'der' and x != 27:
            pos_siguiente = (x+1, y)
        elif self.direccion == 'izq' and x != 0:
            pos_siguiente = (x-1, y)
        elif self.direccion == 'up' and y != 0:
            pos_siguiente = (x, y-1)
        elif self.direccion == 'down' and y != 30:
            pos_siguiente = (x, y+1)
        else:
            return False
        
        if mapa[pos_siguiente] != 'pared':
            return True
        else:
            return False
        
    def movimeinto(self):
        if self.direccion == 'up':
            pos2 = (0, -1 * self.velocidad)
        elif self.direccion == 'right':
            pos2 = (self.velocidad, 0)
        elif self.direccion == 'down':
            pos2 = (0, self.velocidad)
        elif self.direccion == 'left':
            pos2 = (-1 * self.velocidad, 0)
            
        x, y = self.sumar_posiciones((self.posx, self.posy), pos2)
        
        self.posx = x
        self.posy = y


    def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
        return tuple(a + b for a, b in zip(pos1, pos2))