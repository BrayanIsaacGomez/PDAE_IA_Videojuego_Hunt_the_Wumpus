import random
from habitacion import Habitacion

class Mundo:
    def __init__(self, size=4):
        self.size = size
        # Crea una cuadrícula 2D llenándola con objetos del tipo Habitación
        self.grid = [[Habitacion(c, f) for f in range(size)] for c in range(size)]
        self._colocar_peligros_y_tesoro()
    
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////
    
    def _colocar_peligros_y_tesoro(self):
        # 1. Creando una lista con todas las coordenadas posibles
        posiciones_disponibles = []
        for x in range(self.size):
            for y in range(self.size):
                posiciones_disponibles.append((x, y))
                
        # 2. Quitando la casilla de inicio para que siempre sea segura
        posiciones_disponibles.remove((0, 0))

        # 3. Intercambiar las posiciones de los elementos de forma aleatoria
        random.shuffle(posiciones_disponibles)

        # --- Colocando un Monstruo ---
        mx, my = posiciones_disponibles.pop()
        self.grid[mx][my].tiene_monstruo = True
        print(f"  > Monstruo colocado en [{mx},{my}]")

        # --- Colocando el Tesoro ---
        tx, ty = posiciones_disponibles.pop()
        self.grid[tx][ty].tiene_tesoro = True
        print(f"  > Tesoro colocado en [{tx},{ty}]")

        # --- Colocando 2 Pozos ---
        numero_de_pozos = 2
        for i in range(numero_de_pozos):
            if not posiciones_disponibles:
                break
                
            px, py = posiciones_disponibles.pop()
            self.grid[px][py].tiene_pozo = True
            print(f"  > Pozo #{i+1} colocado en [{px},{py}]")
    
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////

    def get_percepts(self, posicion_agente, monstruos_eliminados):
        """
        Devuelve una lista de percepciones para la posición actual del agente.
        """
        x, y = posicion_agente
        percepciones = []

        # 1. Revisa las habitaciones adyacentes para Hedor y Brisa
        # en este orden: Arriba, derecha, abajo, izquierda
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            # Asegurando que son posición dentro del mapa
            if 0 <= nx < self.size and 0 <= ny < self.size:
                habitacion_adyacente = self.grid[nx][ny]
                if habitacion_adyacente.tiene_monstruo and ( [nx,ny] not in monstruos_eliminados):
                    if 'Hedor' not in percepciones:
                        percepciones.append('Hedor')
                if habitacion_adyacente.tiene_pozo:
                    if 'Brisa' not in percepciones:
                        percepciones.append('Brisa')
        
        # 2. Revisa la habitación actual para Brillo (Tesoro) y/o Hedor(Monstruo)
        habitacion_actual = self.grid[x][y]
        if habitacion_actual.tiene_tesoro:
            percepciones.append('Brillo')
        if habitacion_actual.tiene_monstruo:
            percepciones.append('Monstruo')
            
        return percepciones

    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////

    def verificar_muerte(self, posicion, monstruos_eliminados):
        x, y = posicion
        habitacion = self.grid[x][y]
        if habitacion.tiene_monstruo or habitacion.tiene_pozo:
            print(f" La habitacion [{x},{y}]  esta en?: {monstruos_eliminados}")
            if (  [x,y] not in monstruos_eliminados):
                return True
            
            return False
        return False
    
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////
    # ///////////////////////////////////////////////////////////////////

    def __str__(self):
        mapa_string = "**************** MAPA *********************\n"
        # Recorre de forma invertida
        for x in range(self.size - 1, -1, -1):
            mapa_string += f"{x} | "
            
            # Itera sobre las columnas
            for y in range(self.size):
                habitacion = self.grid[x][y]
                mapa_string += " " + str(habitacion) + "  "
            
            mapa_string += "\n"

        mapa_string += "  +" + "----" * self.size + "\n"
        mapa_string += "   "
        for y in range(self.size):
            mapa_string += f"  {y} "
            
        return mapa_string + "\n"

    


        
    
