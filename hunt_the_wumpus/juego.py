import os
import time

from mundo import Mundo
from explorador import Explorador

from colorama import init, Fore, Style

init()


sizeMap = 10
juegos = 50
ganados = 0
perdidos = 0

def limpiar_pantalla(): # Limpiar la terminal
    _ = os.system('cls')


def bienvenida():
    mensaje = """
            
                ===============================================
                |                                             |
                |          B I E N V E N I D O   A            |
                |                                             |
                |   H  U  N  T   T  H  E   W  U  M  P  U  S   |
                |                                             |
                ===============================================
    
    Estás en una cueva oscura y laberíntica.
    Tu misión: Encontrar el tesoro perdido
    
    Armado con solo 2 flechas, debes usar tu ingenio para sobrevivir.
    
    Cuidado con los pozos sin fondo y el mal olor del temible Wumpus...
    
    ¡Buena suerte, cazador!


            A continuación el código de colores para facilitar la 
            comprensión del mapa y conociencia del jugador autónomo   
    """
    print(mensaje)
    m = Fore.BLUE + ' - ' + Fore.WHITE + ": Para habitaciones desconocidas\n"
    m += Fore.BLUE+" S " + Fore.WHITE +": Para habitaciones seguras\n"
    m += Fore.GREEN+" V " + Fore.WHITE +": Para habitaciones visitadas\n"
    m += Fore.YELLOW+" P " + Fore.WHITE + ": Para habitaciones con sospecha de pozo\n"
    m += Fore.YELLOW+" M " + Fore.WHITE + ": Para habitaciones con sospecha del Wumpus\n"
    m += Fore.YELLOW+" ¿?" + Fore.WHITE +": Para habitaciones con sospechas de ambos peligros\n"

    m += Fore.RED+" P " + Fore.WHITE +": Para habitaciones con pozos confirmados\n"
    m += Fore. RED + " M " + Fore.WHITE +": Para habitaciones con Wumpus confirmado\n"
    
    m += Fore.MAGENTA+" V " + Fore.WHITE +": Ruta de retorno óptimo hacia salida en tiempo real"+ "\n"
    
    print(m)
    print("\n\t\t***** Implementado por: Brayan Gomez - 20006187 *****\n\n")

def main():
    limpiar_pantalla()
    bienvenida()
    input("\nPresionar ENTER para empezar la exploración autónomatica...")
    
    
    
    
    for i in range(juegos):
        mundo = Mundo(size=sizeMap)
        explorador = Explorador(world_size=sizeMap)
        game_over = False
        turno = 1

        global ganados
        global perdidos
        
        while not game_over:
            #time.sleep(0.1)
            limpiar_pantalla()
            print(f"********************** TEST # {i+1} ************************")

            print(f"=============== TURNO {turno} ===============\n")

            # Percibir el entorno
            percepciones = mundo.get_percepts(explorador.posActual, explorador.monstruos_eliminados)

            # Actualiar el conocimento del explorador
            res = explorador.actualizar_conocimiento(percepciones)


            if res == 'disparar':
                percepciones = mundo.get_percepts(explorador.posObjetivo, explorador.monstruos_eliminados)
                print(Fore.GREEN + "Disparando... - >  - > - >")
                if 'Monstruo' in percepciones:
                    print(Fore.GREEN + "Le has dado al monstruo")
                    print(Fore.WHITE)
                    explorador.accionDisparar(feedback=True)
                else:
                    explorador.accionDisparar(feedback=False)
                    print(Fore.RED +  "No le has dado al monstruo, el mosntruo no estaba allí .....")
                    print(Fore.WHITE)
                

            # Percibir el entorno
            percepciones = mundo.get_percepts(explorador.posActual, explorador.monstruos_eliminados)

            # Actualiar el conocimento del explorador
            res = explorador.actualizar_conocimiento(percepciones)

            # Mostrar el mapa
            print(mundo)
            print(explorador)
            
            # Mostrarme el estado actual del explorador
            print("\n--- ESTADO DEL EXPLORADOR ---")
            print(Fore.GREEN + " --- ALGORITMO DFS --- " + Fore.WHITE)
            print(f"OBJETIVO ACTUAL: ", end="")
            if explorador.objetivo_actual == 'BUSCAR_ORO':
                m = Fore.YELLOW + "BUSCAR_ORO"+Fore.WHITE
            else:
                m = Fore.BLUE + "VOLVER_A_INICIO"+Fore.WHITE
            print(m)
            print(f"En posición: {explorador.posActual} percibe: {percepciones if percepciones else 'Nada'}")
            

            # Tomar una decisión de ¿QUÉ HACER?
            accion = explorador.decidir_accion()
            print(f"Acción decidida por el explorador: {accion}")
            
            if( explorador.posObjetivo):
                print(f"Objetivo: {explorador.posObjetivo}")
        
        
        
            match accion:
                case 'caminar':
                    explorador.accionCaminar()
                    
                case 'retroceder':
                    explorador.accionRetroceder()
                case 'girar':
                    explorador.accionGirar()
                case 'agarrar':
                    
                    pass
                case 'disparar':
                    percepciones = mundo.get_percepts(explorador.posObjetivo,explorador.monstruos_eliminados)
                    print(Fore.GREEN + "Disparando... - >  - > - >")
                    if 'Monstruo' in percepciones:
                        print(Fore.GREEN + "Le has dado al monstruo")
                        print(Fore.WHITE)
                        explorador.accionDisparar(feedback=True)
                    else:
                        explorador.accionDisparar(feedback=False)
                        print(Fore.RED +  "No le has dado al monstruo, el mosntruo no estaba allí .....")
                        print(Fore.WHITE)
                case 'salir':
                    print(Fore.GREEN + "\n¡El agente ha salido de la cueva con el oro!")
                    print(Fore.WHITE)
                    ganados +=1
                    game_over = True
                case 'ninguna':
                    print("\nEl agente ha terminado su tarea o no tiene más acciones.")
                    game_over = True
                case _:
                    
                    pass
        
            
            
            if not game_over and mundo.verificar_muerte(explorador.posActual, explorador.monstruos_eliminados):
                print( Fore.RED +  f"\n¡GAME OVER! El agente ha muerto en la posición {explorador.posActual}.")
                perdidos += 1
                game_over = True
                print(f"Monstruos eliminados en: {explorador.monstruos_eliminados}")
                
                
            if not game_over:
                
                try:
                    code = int(input("\nPresiona Enter para continuar al siguiente turno..."))
                    if( code == 0 ):
                        break
                except:
                    pass
                
                turno += 1
            
            

            

        print("\n================ FIN DEL TEST ================")
    
    print(Fore.BLUE +"METRICAS DEL JUEGO")
    print(f"TOTAL DE JUEGOS JUGADOS: {juegos}")
    print(f"JUEGOS GANADOS: {ganados}")
    print(f"JUEGOS PERDIDOS: {perdidos}"+Fore.WHITE)

main()


