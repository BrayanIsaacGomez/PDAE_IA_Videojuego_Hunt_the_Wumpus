from habitacion import Habitacion
import random
from colorama import init, Fore

init()


class Explorador:
    def __init__(self, world_size):
        self.world_size = world_size
        
        self.conocimiento = [ [Habitacion(x,y) for y in range(world_size)] for x in range(world_size)]
        self.historial = []
        self.posActual = [0, 0]
        self.posAnterior = [0, 0]
        self.flechasDisponibles = 3
        self.encontroElTesoro = False
        self.UMBRAL_CONFIRMACION = 2 # Peligro confirmado celda sospechosa desde 2 posiciones distintas
        self.sinVisitar = set()
        self.monstruos_eliminados = []
        self.rutaRetorno = []

        # Conocimiento del explorador: cuadrícula de objetos Habitacion.
        self.knowledge_base = [[Habitacion(x, y) for y in range(world_size)] for x in range(world_size)]
        
        # Estado del agente
        self.arrows = 2
        self.tiene_tesoro = False
        
        self.posObjetivo = []

        # Marcar la primera habitación como segura y visitada al inicio.
        start_room = self.knowledge_base[0][0]
        start_room.visitada = True

        self.has_gold = False
        self.objetivo_actual = 'BUSCAR_ORO' # Estados: 'BUSCAR_ORO', 'VOLVER_A_INICIO', 'TERMINADO'

        self.monstruo_confirmado_pos = None
    
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////


    def actualizar_conocimiento(self, percepciones):
        # Puede venir, Brillo, Hedor, Brisa
        x, y = self.posActual
        pos_actual_tupla = tuple(self.posActual)
        # Marcar la primera habitación como segura y visitada al inicio.
        room = self.knowledge_base[x][y]
        room.visitada = True
        if not percepciones:
            
            room.es_segura = True
            
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.world_size and 0 <= ny < self.world_size: # Cuando la posición sea valida
                    room = self.knowledge_base[nx][ny]
                    room.es_segura = True
                    if not room.visitada:
                        self.sinVisitar.add( tuple([nx,ny]) )
                    # Solo aumenta si la sospecha viene de un nuevo lugar
                    if room.sospecha_monstruo or room.sospecha_pozo:
                        if tuple([x,y]) not in room.sospecha_pozo_desde:
                            # Marcar posición como segura
                            room.sospecha_monstruo = 0
                            room.es_segura = True
                        if tuple([x,y]) not in room.sospecha_monstruo_desde:
                            # Marcar posición como segura
                            room.sospecha_monstruo = 0
                            room.es_segura = True
        
        if 'Brillo' in percepciones and not self.has_gold:
            print(Fore.YELLOW +"¡He encontrado el oro! El nuevo objetivo es volver a casa.")
            print(Fore.WHITE)
            room = self.knowledge_base[x][y]
            room.visitada = True
            room.es_segura = True
            self.encontroElTesoro = True
            self.has_gold = True
            self.objetivo_actual = 'VOLVER_A_INICIO'
            

        if 'Brisa' in percepciones:
            room = self.knowledge_base[x][y]
            room.es_segura = True
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.world_size and 0 <= ny < self.world_size: # Cuando la posición sea valida
                    habitacion_sospechosa = self.knowledge_base[nx][ny]
                    # Aumentado valor si la sospecha viene de un nuevo lugar
                    if pos_actual_tupla not in habitacion_sospechosa.sospecha_pozo_desde and ( not habitacion_sospechosa.es_segura ) :
                        habitacion_sospechosa.sospecha_pozo += 1
                        habitacion_sospechosa.sospecha_pozo_desde.add(pos_actual_tupla) # Para evitar duplicados
                        
                        # ¿ Se confirma el peligro?
                        if habitacion_sospechosa.sospecha_pozo >= self.UMBRAL_CONFIRMACION:
                            habitacion_sospechosa.confirmado_pozo = True
                            print(f"¡Pozo confirmado en [{nx},{ny}] por nivel de sospecha!")

        
        if 'Hedor' in percepciones:
            room = self.knowledge_base[x][y]
            room.es_segura = True
            for dx, dy in [(1,0), (0,1), (-1,0), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.world_size and 0 <= ny < self.world_size:
                    habitacion_sospechosa = self.knowledge_base[nx][ny]
                    
                    if pos_actual_tupla not in habitacion_sospechosa.sospecha_monstruo_desde:
                        
                        if ( not habitacion_sospechosa.es_segura ):
                            habitacion_sospechosa.sospecha_monstruo += 1 
                            habitacion_sospechosa.sospecha_monstruo_desde.add(pos_actual_tupla)
                            
                            if habitacion_sospechosa.sospecha_monstruo >= self.UMBRAL_CONFIRMACION:
                                habitacion_sospechosa.confirmado_monstruo = True
                                self.monstruo_confirmado_pos = [nx, ny]     # Guardamos la posición confirmada en el agente para disparar
                                print(f"¡Monstruo confirmado en [{nx},{ny}]!")
                                print(f"Posición del monstruo guardada en el agente: {self.monstruo_confirmado_pos}")
                                
                                self.posObjetivo = [nx,ny]
                                self.historial.append(self.posActual) # Posicion agregada en la última posición
                                
                                return 'disparar'


    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////

    def decidir_accion(self):
        x, y = self.posActual
        if tuple([x,y]) in self.sinVisitar: self.sinVisitar.remove(tuple([x,y]))
        posicionesValidas = [] # Posiciones dentro del mapa
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Este, Oeste, Norte, Sur
            pos = [x + dx, y + dy]
            if (0 <= pos[0] < self.world_size) and (0 <= pos[1] < self.world_size):
                posicionesValidas.append( pos )
        
        r = self.knowledge_base[x][y]
        r.visitada = True

        if self.objetivo_actual == 'BUSCAR_ORO':
            # Si las posiciones adyacentes no se han visitado, y no hay
            # sospecha de pozo o monstruo adyancente
            for coordenada in posicionesValidas:
                nx, ny = coordenada
                room = self.knowledge_base[nx][ny]
                if not room.visitada and not room.sospecha_monstruo and not room.sospecha_pozo:
                    self.posObjetivo = coordenada
                    self.historial.append(self.posActual) # Posicion agregada en la última posición
                    self.posAnterior = self.posActual
                    return 'caminar'
                
            # Retroceder si no se encontro posición desconocida y sin alerta
            # Evaluar si no hay nada en el historial para poder regresar, sino tomar una decsión al azar
            if len(self.historial) > 0:
                # retroceder si hay opciones seguras sn visitar
                habitaciones_sin_explorar = []
                if self.sinVisitar:
                    return 'retroceder'
                else:
                    return self.tomarRiesgo()
            else:
                return self.tomarRiesgo()

            return None

        
        elif self.objetivo_actual == 'VOLVER_A_INICIO':
            sugerencia = self.encontrarRutaRetorno()
            print(Fore.MAGENTA+ "Ruta optima de retorno en tiempo real... --- ALGORITMO A* ---" + Fore.WHITE)
            self.rutaRetorno = sugerencia
            self.historial = sugerencia
            # La función objetivo es: llegar a la celda [0,0]
            # Busca la ruta a la casilla inicial [0,0]
            if self.posActual == [0,0]:
                self.objetivo_actual = 'TERMINADO'
                return 'salir'
            else:
                return 'retroceder'
            

    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////

    def tomarRiesgo(self):
        # Decidir entre las posiciones dentro del mapa, arriba, abajo, izquierda o derecha
        x, y = self.posActual
        posibilidades = [] # Posiciones dentro del mapa
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Este, Oeste, Norte, Sur
            pos = [x + dx, y + dy]
            
            if (0 <= pos[0] < self.world_size) and (0 <= pos[1] < self.world_size):
                room = self.knowledge_base[ pos[0] ][ pos[1] ]
                if ( not room.confirmado_pozo) and ( not room.confirmado_monstruo):
                    posibilidades.append( pos )
        
        posicionElegida = random.choice(posibilidades)

        self.posObjetivo = posicionElegida
        self.historial.append(self.posActual) # Posicion agregada en la última posición
        self.posAnterior = self.posActual
        
        ## Preguntar antes si el peligro es de monstruo y tengo flechas disparar
        room = self.knowledge_base[ self.posObjetivo[0] ][ self.posObjetivo[1] ]
        if room.sospecha_monstruo:
            if self.flechasDisponibles > 0:
                return 'disparar'
            else:
                return 'caminar'
        else:
            return 'caminar'
        
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////

    def encontrarRutaRetorno(self):
        # Implementación del algoritmo A*
        # Para encontrar la ruta óptima de retorno
        posBase= [0,0]
        heuristicas = []
        ruta = []
        ruta.append( posBase )
        posicionesValidas = []
        costoActual = 0
        heuristicaActual = 0
        f = 0
        continuar = True
        while(continuar):
            posicionesValidas.clear()
            heuristicas.clear()
            costoActual += 1
            x,y = posBase
            
            # Convenio de giro a favor de las manecillas del reloj
            # Arriba, Derecha, Abajo, Izquierda
            for dx, dy in [  (1, 0), (0, 1), (-1, 0), (0, -1),]:
                nx, ny = [x + dx, y + dy]

                if [nx,ny] != self.posActual:

                    if (0 <= nx < self.world_size) and (0 <= ny < self.world_size):
                        if [nx,ny] not in ruta:
                            room = self.knowledge_base[ nx][ny]
                            if room.visitada:
                                heuristicaActual = abs( nx - self.posActual[0] ) + abs( ny - self.posActual[1] )
                                f = heuristicaActual + costoActual
                                heuristicas.append(f)
                            else:
                                heuristicas.append( (self.world_size*self.world_size) )
                                
                        else:
                            heuristicas.append( (self.world_size*self.world_size) )
                        
                        posicionesValidas.append( [nx,ny] )
                else:
                    continuar = False
                    break

            if not continuar:
                break     
            
            # Optimizar la función para el menor costo
            s_index = heuristicas.index(min(heuristicas))
            seleccion = posicionesValidas[s_index]
            ruta.append(  seleccion  )
            posBase = seleccion

        return ruta

    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////         

    def accionCaminar(self):
        """Se mueve a la posición objetivo"""
        self.posActual = self.posObjetivo
        self.posObjetivo = None
        
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////

    def accionRetroceder(self):
        self.posObjetivo = None
        self.posAnterior = self.posActual
        #print(f"Historial antes de actualizar posición: {self.historial}")
        if self.sinVisitar and  (self.objetivo_actual == 'BUSCAR_ORO'):
            c = list(self.sinVisitar.pop())
            #print(f"Voy a : {c}")
            self.posActual = c
        else:
            self.posActual = self.historial.pop()

    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////

    def accionDisparar(self, feedback):
        self.flechasDisponibles -= 1
        self.monstruos_eliminados.append( [self.posObjetivo[0], self.posObjetivo[1]   ])
        room = self.knowledge_base[ self.posObjetivo[0] ][self.posObjetivo[1]]
        room.es_segura = True
        room.confirmado_monstruo = False
        room.sospecha_monstruo = False
        room.tiene_monstruo = False
        self.sinVisitar.add( tuple( [self.posObjetivo[0], self.posObjetivo[1] ]) )
        
        self.posObjetivo = None
        

    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////
    # ////////////////////////////////////////////////////////////////////////////////////////////////   
        


    def __str__(self):
        
        #Construye una representación en string de la base de conocimiento del agente.
        
        ancho_celda = 2  # ancho fijo para cada celda
        mapa_string = "********** CONOCIMIENTO DEL EXPLORADOR ****************\n"
        colorEspecial = False
        for x in range(self.world_size - 1, -1, -1):
            mapa_string += f"{x:>2} |"  # número de fila alineado a la derecha
            for y in range(self.world_size):
                habitacion = self.knowledge_base[x][y]
                colorEspecial = False
                if [x,y] in self.rutaRetorno:
                    colorEspecial = True
                vista = habitacion.get_vista_agente(colorEspecial)
                if self.posActual == [x,y]:
                    vista = Fore.MAGENTA + " ☺ " + Fore.WHITE
                
                mapa_string += f"{vista:^{ancho_celda}}"  # contenido centrado en la celda
            mapa_string += "\n"

        # Línea inferior del mapa
        mapa_string += "   +" + ("-" * ancho_celda) * self.world_size + "\n"

        # Números de columna
        mapa_string += "    "  # Espacio inicial debajo de los índices de fila
        for y in range(self.world_size):
            mapa_string += f"{y:^{ancho_celda}}"
            
        return mapa_string