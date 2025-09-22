#  Hunt the Wumpus - Proyecto de Inteligencia Artificial 🏹

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)

Este repositorio contiene una implementación del clásico juego "Hunt the Wumpus", desarrollado como proyecto final para el curso de Inteligencia Artificial. El objetivo es demostrar la aplicación del conocimiento recibido durante el curso, así como el uso de algoritmos para el desarrollo de solución a problemas específicos.

Se implementó el uso de algoritmos de búsqueda informada y no informada para la exploración y navegación de un agente inteligente en un entorno desconocido y peligroso.

## ✨ Características Principales

* **Diseño Orientado a Objetos:** El código está estructurado en clases (`Mapa`, `Explorador`, `Habitacion`) para una mayor claridad y mantenibilidad.
* **Exploración Inteligente:** El agente explora la cueva de forma autónoma utilizando un algoritmo de **Búsqueda en Profundidad (DFS)**.
* **Ruta de Escape Óptima:** Una vez que el agente tiene el tesoro, utiliza el algoritmo **A\* (A-Star)** para encontrar el camino más corto y seguro de regreso a la entrada a través de las habitaciónes ya visitadas.
* **Juego Clásico:** Incluye todos elementos icónicos: el Wumpus, pozos sin fondo y el tesoro.

## 🐍 Tecnologías Utilizadas

* **Python 3**
* Programación Orientada a Objetos (POO)

## ⚙️ Instalación y Ejecución

El proyecto no requiere bibliotecas externas, solo una versión estándar de Python 3.

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/BrayanIsaacGomez/PDAE_IA_Videojuego_Hunt_the_Wumpus.git](https://github.com/BrayanIsaacGomez/PDAE_IA_Videojuego_Hunt_the_Wumpus.git)
    cd PDAE_IA_Videojuego_Hunt_the_Wumpus
    ```

2.  **Ejecuta el archivo principal:**
    ```bash
    python juego.py
    ```

## 🧠 Algoritmos Implementados

Este proyecto se centra en la aplicación de dos tipos de algoritmos de búsqueda fundamentales en la IA.

### 1. Búsqueda No Informada: Depth-First Search (DFS)

Para la fase de exploración, el agente no tiene conocimiento previo del mapa. Se utiliza **DFS** para navegar por la cueva de manera sistemática.

* **Propósito:** Explorar lo más profundo posible por cada camino para descubrir la topología de la cueva en búsqueda del tesoro y la ubicación de los peligros para futuras decisiones mas inteligentes.
* **Implementación:** El agente avanza de una `Habitacion` a otra, marcando las visitadas para no caer en bucles, retrocede (backtracking) cuando llega a un callejón sin salida o toma una decisión riesgosa en caso no tener mas opciones viables.

### 2. Búsqueda Informada: A\* Pathfinding

Una vez que el explorador ha recogido el oro, su objetivo es regresar a la entrada `[0,0]` por la ruta más segura y corta posible.

* **Propósito:** Calcular el camino óptimo de regreso utilizando el conocimiento adquirido del mapa.
* **Implementación:** Se utiliza **A\***, que combina el costo real del camino recorrido (`g(n)`) con una heurística (distancia de Manhattan) para estimar el costo restante (`h(n)`). Esto garantiza encontrar el camino más corto en el menor tiempo posible, resolviendo este desafío de una forma "relajada".

## 🏛️ Estructura del Código (POO)

El diseño del software se basa en los siguientes componentes principales:

* **`Habitacion`**: Representa una única celda en la cueva. Almacena información sobre si contiene un peligro (Wumpus, pozo), una percepción (brisa, hedor) o si es segura y/o ha sido visitada.
* **`Mapa`**: Gestiona la colección de objetos `Habitacion` y las conexiones entre ellas, formando el laberinto.
* **`Explorador`**: Es el agente inteligente. Mantiene su estado actual (posición, flechas), interactúa con el `Mapa` y contiene la lógica para los algoritmos de búsqueda (DFS y A\*).

## 🎯 Demo del Juego

¡Explora el proceso de desarrollo y las demostraciones de este proyecto en la playlist oficial de YouTube!

[![Miniatura de la Playlist](https://i.ytimg.com/pl_c/PLp0enpagyuznbeSGIcl1MefFM5z9PsUIg/studio_square_thumbnail.jpg?sqp=COSkxcYG-oaymwEICKoDEPABSFqi85f_AwYI5b7FxgY=&rs=AOn4CLAKL04mwZ3IoMbOLB-BFtaun5QwCw)](https://www.youtube.com/playlist?list=PLp0enpagyuznbeSGIcl1MefFM5z9PsUIg)

También puedes acceder directamente aquí: [Ver Playlist en YouTube](https://www.youtube.com/playlist?list=PLp0enpagyuznbeSGIcl1MefFM5z9PsUIg)
