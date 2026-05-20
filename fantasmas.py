class fantasma:
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
        
    def movimiento(self, x: int, y: int):
        self.pos_x += x
        self.pos_y += y
        
    def cambio_direccion(self, angulo: int):
        self.angulo_futuro = angulo
        
    def turno(self):
        if self == True and self.angulo_futuro != self.direccion:
            self.direccion = self.angulo_futuro    
