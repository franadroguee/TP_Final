from math import sqrt

def sumar_posiciones(pos1: tuple, pos2: tuple) -> tuple:
    """
    Obtiene dos tuplas con coordenadas y las suma
    """
    
    return tuple(a + b for a, b in zip(pos1, pos2))

def distancia(pos1: tuple, pos2: tuple) -> float:
    """
    Calcula la distancia diagonal entre dos casillas
    """
    
    x1, y1 = pos1
    x2, y2 = pos2
    
    dist_X = abs(x2 - x1)
    dist_y = abs(y2 - y1)
    
    return sqrt(dist_X**2 + dist_y**2)

class personaje:
    def __init__(self, posx:int, posy: int, velocidad: float) -> None:
        '''
        Define su posicion, direccion y velocidad
        '''
        
        self.posx = posx
        self.posy = posy
        self.direccion = 'right' # 'right', 'left', 'up', 'down'
        self.direccion_deseada = 'right'
        self.velocidad = velocidad
        self.casilla = (posx/20, posy/20) # se actualiza cuando el personaje esta centrado
    
    def movimeinto(self) -> None:
        """
        Altera self.posx, self.posy en funcion de la direccion del personaje. Si esta por salirse de una casilla, antes de hacerlo, se centra en la misma.
        """
        
        # primero calcula la celda x e y del personaje a pesar de que no este centrado
        celdax = int(self.posx//20) + 1 if (self.posx % 20) > 10 else int(self.posx // 20) 
        celday = int(self.posy//20) + 1 if (self.posy % 20) > 10 else int(self.posy // 20)
        
        if self.direccion == 'up':
            if self.posy < (celday * 20) and (celday *20) < self.posy + self.velocidad: # en caso de que el personaje este a punto de salirse de la celda, sin haber estado centrado en ella, limita su velocidad durante 1 frame para que este contenido en la casilla
                pos2 = (0, -(self.posy - (celday *20)))
            else:
                pos2 = (0, -self.velocidad) # si no esta a punto de salirse de su casilla, se mueve a velocidad normal
                
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
    
    def cambiar_velocidad(self, nueva_velocidad: int) -> None:
        """
        Altera la velocidad del personaje
        """
        
        self.velocidad = nueva_velocidad
        
    def posicion_perfecta(self) -> bool:
        '''
        Devuelve True si la entidad esta ubicada en el centro de una casilla.
        '''
        
        if self.posx % 20 == 0 and self.posy % 20 == 0: 
            # en caso de que el resto de dividir la posicion del personaje por 20 sea 0, se sabe que esta centrado en una casilla
            return True
        else:
            return False
        
    def chequeo_tunel(self, mapa: dict) -> None: 
        """
        A ejecutarse con el personaje centrado. Revisa si su posicion es un tunel. De serlo, altera su posx, posy a la posicion del otro tunel en el mapa
        """
        
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

class pacman(personaje):
    def __init__(self, posx, posy, velocidad) -> None:
        super().__init__(posx, posy, velocidad)
        
    def puede_cambiar_direccion(self, mapa: dict) -> bool:
        """
        Analiza los obstaculos en el mapa para establecer si el personaje puede o no cambiar de direccion
        """
        
        if self.posicion_perfecta():
            x = int(self.posx / 20) # al estar centrado, la division de su posicion por 20 tendra resto 0
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
            return False

        
    def cambio_direccion(self) -> None:
        """
        Dirije al personaje en la direccion en la que deseaba ir 
        """
        
        self.direccion = self.direccion_deseada

    def analisis_comer(self, mapa: dict, puntaje) -> dict | int | bool:
        """
        A ejecutarse cuando el personaje esta centrado en una casilla. Si la casilla tiene un comestible (punto, powerpellet), lo remueve del mapa y registra la accion
        """
        
        x = int(self.posx / 20)
        y = int(self.posy / 20)
        
        comio_powerpellet = False
        if mapa[(x, y)] == 'punto': 
            mapa[(x, y)] = 'pasillo' # remueve el punto del mapa
            puntaje += 10 # suma 10 puntos por el consumible "punto"
        elif  mapa[(x, y)] == 'power':
            mapa[(x, y)] = 'pasillo'
            puntaje += 20 # suma 20 puntos por el consumible "PowerPellet"
            comio_powerpellet = True
            
        return mapa, puntaje, comio_powerpellet            
        
    def debe_moverse(self, mapa:dict) -> bool:
        """
        A ejecutarse cuando el personaje esta centrado en una casilla. Si la casilla siguiente en la direccion que esta yendo es un obstaculo, retorna False. De no serlo, retorna True.
        """
        
        if self.posicion_perfecta():
            x = int(self.posx / 20) # dado que el personaje esta centrado, la division siempre devolvera un numero redondo
            y = int(self.posy / 20)
            
            if self.direccion == 'right':
                siguiente_casilla = (x+1, y) # 1 casilla a la derecha
            elif self.direccion == 'left':
                siguiente_casilla = (x-1, y) # 1 casilla a la izquierda
            elif self.direccion == 'up':
                siguiente_casilla = (x, y-1) # 1 casilla arriba
            elif self.direccion == 'down':
                siguiente_casilla = (x, y+1) # una casilla abajo
                
            if mapa[siguiente_casilla] == 'pared' or mapa[siguiente_casilla] == 'puerta': # dado que el personaje esta centrado, se puede saber facilmente cual sera la siguiente casilla en la que estara en funcion de su direccion.
                return False
            else: 
                return True # no hay obstaculos
        
        else:
            return True
        
    def recepcion_input(self, tecla) -> None:
        """
        Establece la direccion deseada del personaje a la tecla oprimida por el jugador
        """
        
        self.direccion_deseada = tecla
        
    def frame_pacman(self, mapa: dict, puntaje: int) -> dict | int | bool:
        """
        Se ejecuta todos los frames. Procesa todas las acciones del personaje (movimiento, comestibles, etc.). Devuelve el diccionario con el mapa actualizado y el nuevo puntaje del jugador
        """
        comio_powerpellet = False
        if self.direccion_deseada != self.direccion and self.puede_cambiar_direccion(mapa):
            # si pacman desea ir en una direccion distinta a la que esta yendo y esta centrado
            self.cambio_direccion()
            
        if self.debe_moverse(mapa):
            self.movimeinto()
            
        if self.posicion_perfecta():
            self.casilla = (self.posx/20, self.posy/20)
            mapa, puntaje, comio_powerpellet = self.analisis_comer(mapa, puntaje)
            self.chequeo_tunel(mapa)
            
        return mapa, puntaje, comio_powerpellet

class fantasma(personaje):
    def __init__(self, posx, posy, velocidad, nombre):
        super().__init__(posx, posy, velocidad)
        self.nombre = nombre
        self.salio_house = False
        self.modo = 'scatter' # scatter, chase, scare

    def frame_ghost(self, ghost_places: list, mapa: dict, info_bots: tuple, grafico, pantalla) -> None:
        if self.posicion_perfecta():
            self.casilla = (self.posx/20, self.posy/20)
            
        if self.casilla not in ghost_places:
            self.salio_house = True
            
        if not self.salio_house:    
            self.direccion = self.dirigirse_a_casilla((14, 0), mapa)
            pantalla.blit(grafico, (self.posx, self.posy))
            return None
                     
        if self.posicion_perfecta():
            self.chequeo_tunel(mapa)
            if self.modo == 'scatter':
                self.scatter((0, 0), mapa)
            elif self.modo == 'chase':
                if self.nombre == 'blinky':
                    self.direccion = self.blinky_chase(info_bots, mapa)
                elif self.nombre == 'pinky':
                    self.direccion = self.pinky_chase(info_bots, mapa)
            else:
                pos_pacman = info_bots[0]
                self.scared(pos_pacman, mapa)            
                        
        if self.debe_moverse(mapa):
            self.movimeinto()
            
        pantalla.blit(grafico, (self.posx, self.posy))
        
    def debe_moverse(self, mapa:dict) -> bool:
        """
        A ejecutarse con el personaje centrado. Analiza el mapa para ver si la proxima casilla es un obstaculo de serlo retorna False. De no serlo retorna True
        """
        
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
            
            if not self.salio_house and mapa[siguiente_casilla] == 'puerta':
                return True
            
            if mapa[siguiente_casilla] == 'pared' or mapa[siguiente_casilla] == 'puerta':
                return False
            else:
                return True
        
        else:
            return True

    def dirigirse_a_casilla(self, objetivo: tuple, mapa: dict) -> str:
        """
        Recibe un tile objetivo y calcula, teniendo en cuenta los obstaculos del mapa, que direccion es la mas optima para acercarse a su tile objetivo. No habilita el cambio de direccion
        """

        x = (self.posx)/20
        y = (self.posy)/20
        
        direcciones_disponibles = []
        direccion_opuesta = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        direcciones_posibles = {'left': (int(x-1), int(y)), 'right': (int(x+1), int(y)), 'up': (int(x), int(y-1)), 'down': (int(x), int(y+1))}
        
        direcciones_posibles.pop(direccion_opuesta[self.direccion])
        
        for dir, casilla in direcciones_posibles.items():
            
            if not self.salio_house and mapa[casilla] == 'puerta':
                direcciones_disponibles.append((dir, casilla))

            if mapa[(casilla)] != 'pared' and mapa[casilla] != 'puerta':
                direcciones_disponibles.append((dir, casilla))
                
        
        dist_min = float('inf')
        for dir, casilla in direcciones_disponibles:
            dist = distancia(casilla, (objetivo))
            if dist < dist_min:
                dir_min = dir
                dist_min = dist
                
        return dir_min
 
    def scatter(self, esquina, mapa) -> str:
        """
        Recibe la esquina en la que el fantasma ejecuta "scatter" y dirije al fantasma hacia ella mediante la direccion contenida en un str.
        """
        
        return self.dirigirse_a_casilla(esquina, mapa)

    def blinky_chase(self, info_pacman: tuple, mapa: dict) -> str:
        """
        Recibe la posicion del fantasma cuando este esta centrado en una casilla y devuelve un string con la direccion que debe tomar para dirigirse a su casilla de destino.
        """
        
        pac_pos = info_pacman[0]
                        
        return self.dirigirse_a_casilla(pac_pos, mapa)
    
    def pinky_chase(self, info_pacman: tuple, mapa: dict) -> str:
        """
        Recibe la posicion del fantasma cuando este esta centrado en una casilla y devuelve un string con la direccion que debe tomar para dirigirse a su casilla de destino.
        """
            
        tiles_direccion = {'right': (4, 0), 'left': (-4, 0), 'up': (0, -4), 'down': (0, 4)}
        pac_pos, pac_dir = info_pacman
        pac_x, pac_y = pac_pos
        if pac_dir == None:
            suma = (0, 0)
        else:
            suma = tiles_direccion[pac_dir]
        
        obj = sumar_posiciones((pac_x, pac_y), (suma))
        
        return self.dirigirse_a_casilla(obj, mapa)
    
    def scared(self, pos_pacman, mapa):
        """
        Recibe la posicion de Pac_man y calcula que direccion le permite alejarse mas de este.
        """

        x = (self.posx)/20
        y = (self.posy)/20
        
        direcciones_disponibles = []
        direccion_opuesta = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        direcciones_posibles = {'left': (int(x-1), int(y)), 'right': (int(x+1), int(y)), 'up': (int(x), int(y-1)), 'down': (int(x), int(y+1))}
        
        direcciones_posibles.pop(direccion_opuesta[self.direccion])
        
        for dir, casilla in direcciones_posibles.items():
            
            if not self.salio_house and mapa[casilla] == 'puerta':
                direcciones_disponibles.append((dir, casilla))

            if mapa[(casilla)] != 'pared' and mapa[casilla] != 'puerta':
                direcciones_disponibles.append((dir, casilla))
                
        
        dist_min = float(0)
        for dir, casilla in direcciones_disponibles:
            dist = distancia(casilla, (pos_pacman))
            if dist > dist_min:
                dir_min = dir
                dist_min = dist
                
        return dir_min

    def cambio_de_modo(self, nuevo_modo: str) -> None:
        """
        Cambia el modo del fantasma al modo deseado (scatter, chase, scare). Al hacerlo, el fantasma invierte su direccion
        """
        
        direcciones_opuestas = {'right': 'left', 'left': 'right', 'up': 'down', 'down': 'up'}
        
        direccion_opuesta = direcciones_opuestas[self.direccion]
        self.direccion = direccion_opuesta
        self.modo = nuevo_modo