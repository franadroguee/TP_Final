def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
    return tuple(a + b for a, b in zip(pos1, pos2))
    
class personaje:
    def __init__(self, posx:int, posy: int, velocidad: float):
        '''
        Define su posicion, direccion y velocidad
        '''
        
        self.posx = posx
        self.posy = posy
        self.direccion = 'right' # 'right', 'left', 'up', 'down'
        self.direccion_deseada = 'right'
        self.velocidad = velocidad
    
    def movimeinto(self):
        if self.direccion == 'up':
            pos2 = (0, -1 * self.velocidad)
        elif self.direccion == 'right':
            pos2 = (self.velocidad, 0)
        elif self.direccion == 'down':
            pos2 = (0, self.velocidad)
        elif self.direccion == 'left':
            pos2 = (-1 * self.velocidad, 0)
            
        x2, y2 = pos2
        pos_final = sumar_posiciones((self.posx, self.posy), (x2, y2))
        
        x, y = pos_final
        self.posx = x
        self.posy = y
    
    def cambio_direccion(self):
        self.direccion = self.direccion_deseada
    
    def cambiar_velocidad(self, nueva_velocidad: int):
        self.velocidad = nueva_velocidad
        
    def posicion_perfecta(self) -> bool:
        '''
        Devuelve True si la entidad esta ubicada en el centro de una casilla.
        '''
        
        if self.posx % 20 == 0 and self.posy % 20 == 0:
            return True
        else:
            return False
        
    def puede_cambiar_direccion(self, mapa) -> bool:
        if self.posicion_perfecta():
            x = int(self.posx / 20)
            y = int(self.posy / 20)
            
            if self.direccion_deseada == 'right':
                siguiente_casilla = (x+1, y)
            elif self.direccion_deseada == 'left':
                siguiente_casilla = (x-1, y)
            elif self.direccion_deseada == 'up':
                siguiente_casilla = (x, y-1)
            elif self.direccion_deseada == 'down':
                siguiente_casilla = (x, y+1)
                
            if mapa[siguiente_casilla] == 'pared':
                return False
            else:
                return True
        
        else:
            return True

    
    def debe_moverse(self, mapa:dict) -> bool:
        if self.posicion_perfecta():
            x = int(self.posx / 20)
            y = int(self.posy / 20)
            
            if self.direccion == 'right':
                siguiente_casilla = (x+1, y)
            elif self.direccion == 'left':
                siguiente_casilla = (x-1, y)
            elif self.direccion == 'up':
                siguiente_casilla = (x, y-1)
            elif self.direccion == 'down':
                siguiente_casilla = (x, y+1)
                
            if mapa[siguiente_casilla] == 'pared':
                return False
            else:
                return True
        
        else:
            return True
        
    def frame(self, mapa):
        if self.direccion_deseada != self.direccion and self.posicion_perfecta() and self.puede_cambiar_direccion(mapa):
            self.cambio_direccion()
            
        if self.debe_moverse(mapa):
            self.movimeinto()
            
            

class pacman(personaje):
    def __init__(self, posx, posy, velocidad):
        super().__init__(posx, posy, velocidad)
        
    def recepcion_input(self, tecla):
        self.direccion_deseada = tecla
