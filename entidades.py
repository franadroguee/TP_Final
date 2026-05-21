class entidad:
    def __init__(self, posx, posy, velocidad):
        self.posx = posx
        self.posy = posy
        self.direccion = 90
        self.direccion_deseada = 0
        self.velocidad = velocidad
    
    def cambiar_velocidad(self, nueva_velocidad: int):
        self.velocidad = nueva_velocidad
        
    def movimeinto(self):
        if self.direccion == 0:
            pos2 = (0, -1 * self.velocidad)
        elif self.direccion == 90:
            pos2 = (self.velocidad, 0)
        elif self.direccion == 180:
            pos2 = (0, self.velocidad)
        elif self.direccion == 270:
            pos2 = (-1 * self.velocidad, 0)
            
        x, y = self.sumar_posiciones((self.posx, self.posy), pos2)
        
        self.posx = x
        self.posy = y


    def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
        return tuple(a + b for a, b in zip(pos1, pos2))