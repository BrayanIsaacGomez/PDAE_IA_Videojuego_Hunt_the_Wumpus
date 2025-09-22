from colorama import Fore

class Habitacion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # --- Atributos del Mundo Real (Ground Truth) ---
        self.tiene_monstruo = False
        self.tiene_pozo = False
        self.tiene_tesoro = False
        
        # --- Atributos de la Base de Conocimiento del Agente ---
        # El agente usará su propia copia de estas cuevas para guardar lo que cree
        self.visitada = False
        self.es_segura = False
        self.sospecha_pozo = False
        self.sospecha_monstruo = False
        self.confirmado_pozo = False
        self.confirmado_monstruo = False
        
        self.sospecha_pozo_desde = set() # Usado para no almacenar duplicados
        self.sospecha_monstruo_desde = set() # Guarda las tuplas desde donde vino la sospecha
        

        self.nivel_sospecha_pozo = 0
        self.nivel_sospecha_monstruo = 0
    
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    
    def _getAlertasPozo(self):
        return self.nivel_sospecha_monstruo
    
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////

    def _actualizarAlertasPozo(self, pos):
        self.nivel_sospecha_pozo(pos)
        
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    
    def _getAlertasMonstruo(self):
        return self.nivel_sospecha_monstruo

    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////

    def _actualiarAlertasMonstruo(self, pos):
        self.nivel_sospecha_monstruo(pos)
    
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////

    def __str__(self):
        # Un método simple para imprimir el estado de la cueva
        # Para el agente
        if self.confirmado_monstruo: return "¡M!" # Rojo
        if self.confirmado_pozo: return "¡P!" # Rojo
        if self.es_segura: return "S" # Azul
        if self.visitada: return "V" # Verde
        if self.sospecha_pozo: return "¿P?" # Amarillo
        if self.sospecha_monstruo: return "¿M?" # Amarillo

        # Para el mapa
        if self.tiene_monstruo: return Fore. RED + "M" + Fore.WHITE # Rojo
        if self.tiene_pozo: return Fore.RED+"P" + Fore.WHITE # Rojo
        if self.tiene_tesoro: return Fore. YELLOW + "T" + Fore.WHITE  # Amarillo
        return "-" # Desconocida
    
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    # //////////////////////////////////////////////////////////////
    
    def get_vista_agente(self, colorRutaRetorno):
        """
        Devuelve la representación en string de la habitación
        desde el punto de vista del agente.
        """
        m = ''
        if self.confirmado_monstruo:
            m = Fore. RED + " M " + Fore.WHITE # Rojo
            return m
        if self.confirmado_pozo:
            m = Fore.RED+" P " + Fore.WHITE # Rojo
            return m
        if self.es_segura:
            m = Fore.BLUE+" S " + Fore.WHITE # Amarillo advertencia
        if self.visitada:
            m = Fore.GREEN+" V " + Fore.WHITE # Amarillo advertencia
            if colorRutaRetorno:
                m = Fore.MAGENTA+" V " + Fore.WHITE # Amarillo advertencia
        if self.sospecha_monstruo and self.sospecha_pozo and not self.es_segura:
            m = Fore.YELLOW+" ¿?" + Fore.WHITE # Amarillo advertencia
            return m
        if self.sospecha_monstruo and not self.es_segura:
            m = Fore.YELLOW+" M " + Fore.WHITE # Amarillo advertencia
            return m
        if self.sospecha_pozo and not self.es_segura:
            m = Fore.YELLOW+" P " + Fore.WHITE # Amarillo advertencia
            return m
        
        if m == '':
            m = Fore.BLUE + ' - ' + Fore.WHITE
        return m