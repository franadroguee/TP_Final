from math import sqrt

def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
    return tuple(a + b for a, b in zip(pos1, pos2))

def distancia(pos1: tuple, pos2: tuple) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    
    dist_X = abs(x2 - x1)
    dist_y = abs(y2 - y1)
    
    return sqrt(dist_X**2 + dist_y**2)

    
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
        celdax = int(self.posx//20) + 1 if (self.posx % 20) > 10 else int(self.posx // 20)
        celday = int(self.posy//20) + 1 if (self.posy % 20) > 10 else int(self.posy // 20)
        
        if self.direccion == 'up':
            if self.posy < (celday * 20) and (celday *20) < self.posy + self.velocidad:
                pos2 = (0, -(self.posy - (celday *20)))
            else:
                pos2 = (0, -self.velocidad)           
        elif self.direccion == 'right':
            if self.posx < (celdax * 20) and (celdax *20) < self.posx + self.velocidad:
                pos2 = ((celdax*20)-self.posx, 0)
            else:
                pos2 = (self.velocidad, 0)           
        elif self.direccion == 'down':
            if self.posy < (celday * 20) and (celday *20) < self.posy + self.velocidad:
                pos2 = (0, (celday*20)-self.posy)
            else:
                pos2 = (0, self.velocidad)           
        elif self.direccion == 'left':
            if self.posx < (celdax * 20) and (celdax *20) < self.posx + self.velocidad:
                pos2 = (-(self.posx - (celdax *20)), 0)
            else:
                pos2 = (-self.velocidad, 0)           
            
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
                
            if mapa[siguiente_casilla] == 'pared' or mapa[siguiente_casilla] == 'puerta' or mapa[siguiente_casilla] == 'tunel':
                return False
            else:
                return True
        
        else:
            return True

    def tunel(self, mapa: dict): 
        x = int(self.posx / 20)
        y = int(self.posy / 20)
        
        if mapa[(x, y)] == 'tunel':
            tuneles = []
            if self.direccion == 'right':
                pos2 = (20, 0)
            elif self .direccion == 'left':
                pos2 = (-20, 0)
            elif self .direccion == 'up':
                pos2 = (0, -20)
            elif self .direccion == 'down':
                pos2 = (0, 20)

            sumx, sumy = pos2
            
            for numero, casilla in mapa.items():
                if casilla == 'tunel':
                    tuneles.append(numero)
            
            for numero in tuneles:
                tx, ty = numero
                if (tx, ty) != (x, y):
                    self.posx = (tx * 20) + sumx
                    self.posy = (ty * 20) + sumy
    
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
                
            if mapa[siguiente_casilla] == 'pared' or mapa[siguiente_casilla] == 'puerta':
                return False
            else:
                return True
        
        else:
            return True
        
    def analisis_comer(self, mapa: dict, puntaje):
        x = int(self.posx / 20)
        y = int(self.posy / 20)
        
        if mapa[(x, y)] == 'punto':
            mapa[(x, y)] = 'pasillo'
            puntaje += 10
        elif  mapa[(x, y)] == 'power':
            mapa[(x, y)] = 'pasillo'
            puntaje += 20
        return mapa, puntaje                 

class pacman(personaje):
    def __init__(self, posx, posy, velocidad):
        super().__init__(posx, posy, velocidad)
        
    def recepcion_input(self, tecla):
        self.direccion_deseada = tecla
        
    def frame_pacman(self, mapa, puntaje):
        if self.direccion_deseada != self.direccion and self.posicion_perfecta() and self.puede_cambiar_direccion(mapa):
            self.cambio_direccion()
            
        if self.debe_moverse(mapa):
            self.movimeinto()
            
        if self.posicion_perfecta():
            mapa, puntaje = self.analisis_comer(mapa, puntaje)
            self.tunel(mapa)
            
        return mapa, puntaje


class fantasma(personaje):
    def __init__(self, posx, posy, velocidad, nombre):
        super().__init__(posx, posy, velocidad)
        self.nombre = nombre

    def blinky(self, info_pacman: tuple, mapa: dict) -> str:
        """
        Recibe la posicion del fantasma cuando este esta centrado en una casilla y devuelve un string con la direccion que debe tomar para dirigirse a su casilla de destino.
        """
        
        x = (self.posx)/20
        y = (self.posy)/20
        
        pac_pos, pac_dir = info_pacman
        pac_x, pac_y = pac_pos
        
        direcciones_disponibles = []
        direcciones_posibles = {'left': (int(x-1), int(y)), 'right': (int(x+1), int(y)), 'up': (int(x), int(y-1)), 'down': (int(x), int(y+1))}
        
        for dir, casilla in direcciones_posibles.items():
            if mapa[(casilla)] != 'pared':
                direcciones_disponibles.append((dir, casilla))
                
        dist_min = float('inf')
        for dir, casilla in direcciones_disponibles:
            if distancia(casilla, (pac_x/20, pac_y/20)) < dist_min:
                dir_min = dir
                
        return dir_min

    def frame_ghost(self, mapa, info_pacman):
        if self.direccion_deseada != self.direccion and self.posicion_perfecta() and self.puede_cambiar_direccion(mapa):
            self.cambio_direccion()
            
        if self.debe_moverse(mapa):
            self.movimeinto()
            
        if self.posicion_perfecta():
            self.direccion = self.blinky(info_pacman, mapa)
        
