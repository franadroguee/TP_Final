class entidad:
    def __init__(self, posx, posy, velocidad):
        '''
        Define su posicion, direccion y velocidad
        '''
        
        self.posx = posx
        self.posy = posy
        self.direccion = 'right' # 'right', 'left', 'up', 'down'
        self.direccion_deseada = 0
        self.velocidad = velocidad
    
    def cambiar_velocidad(self, nueva_velocidad: int):
        self.velocidad = nueva_velocidad
        
    def posicion_perfecta(self) -> bool:
        '''
        Devuelve True si la entidad esta ubicada en el centro de una casilla.
        '''
        
        if self.posx % 25 == 0 and self.posy % 25 == 0:
            return True
        else:
            return False
        
    def cambio_direccion(self, mapa):
        '''
        Devuelve True cuando puede cambiar de direccion. False cuando no esta centrado en una casilla o no puede tomar la direccion que desea.
        '''
        
        if self.posicion_perfecta():
            return self.puede_moverse(mapa, self.direccion_deseada)
        else:
            return False
            
        
    def puede_moverse(self, mapa:dict, direccion_deseada = '') -> bool:
        if direccion_deseada == '':
            angulo = self.direccion
        else: 
            angulo = direccion_deseada
            
        x = self.posx / 25
        y = self.posy / 25
        
        if angulo == 'der' and x != 27:
            pos_siguiente = (x+1, y)
        elif angulo == 'izq' and x != 0:
            pos_siguiente = (x-1, y)
        elif angulo == 'up' and y != 0:
            pos_siguiente = (x, y-1)
        elif angulo == 'down' and y != 30:
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
            
        x, y = self.sumar_posiciones((self.posx, self.posy), tuple(pos2))
        
        self.posx = x
        self.posy = y


    def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
        return tuple(a + b for a, b in zip(pos1, pos2))
    
class pacman(entidad):
    def __init__(self, posx, posy, velocidad):
        super().__init__(posx, posy, velocidad)
        
    def recepcion_input(self, tecla):
        self.direccion_deseada = tecla
