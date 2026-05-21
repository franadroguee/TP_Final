class entidad:
    def __init__(self, x, y, angulo): # a es el angulo del fantasma. 0 = N, 90 = E, etc.
        '''
        define el objeto fantasma, con su posicion x, su posicion y & el angulo en el que se esta moviendo.
        el angulo 0 representa Norte, 90 representa Este, etc.       
        '''
        
        self.pos_x = x
        self.pos_y = y
        self.direccion = angulo
        self.angulo_futuro = 0
        
    def __bool__(self): # devuelve True si su posicion es una casilla perfecta (x & y son divisibles por 25)
        '''
        Devuelve el valor True si el fantasma esta en una casilla perfecta
        '''
        
        x, y = self.pos
        if x % 25 == 0 and y % 25 == 0:
            return True
        else:
            return False
        
    def movimiento(self, cantidad, angulo):
        if self.direccion
        
    def cambio_direccion(self, angulo: int):
        self.angulo_futuro = angulo
        
    def posibilidad_movimiento(self, mapa: dict):
        x = self.pos_x / 25
        y = self.pos_y / 25
        
        if self.direccion == 0:
            try:
                mov_siguiente = mapa[(int(x), int(y-1))]
                if mov_siguiente != 'pasillo' and mov_siguiente != 'dot':
                    return False
                else:
                    return True
            except:
                return False
        elif self.direccion == 90:
            try:
                mov_siguiente = mapa[(int(x+1), int(y))]
                if mov_siguiente != 'pasillo' and mov_siguiente != 'dot':
                    return False
                else:
                    return True
            except:
                return False

        elif self.direccion == 180:
            try:
                mov_siguiente = mapa[(int(x), int(y+1))]
                if mov_siguiente != 'pasillo' and mov_siguiente != 'dot':
                    return False
                else:
                    return True
            except:
                return False
        elif self.direccion == 270:
            try:
                mov_siguiente = mapa[(int(x-1), int(y))]
                if mov_siguiente != 'pasillo' and mov_siguiente != 'dot':
                    return False
                else:
                    return True
            except:
                return False
        
    def turno(self, velocidad, mapa):
        if self == True:
            if self.angulo_futuro != self.direccion:
                self.direccion = self.angulo_futuro
        
        if self.posibilidad_movimiento(mapa):
            if self.direccion == 0:
                self.pos_y -= velocidad
            elif self.direccion == 90:
                self.pos_x += velocidad
            elif self.direccion == 180:
                self.pos_y += velocidad
            elif self.direccion == 270:
                self.pos_x -= velocidad

class pacman(entidad):
    def __init__(self, x, y, angulo):
        super().__init__(x, y, angulo)
        
pacman1 = pacman(0, 0, 90)

pacman1.movimiento(5, 10)
print(pacman1.pos_x, pacman1.pos_y)