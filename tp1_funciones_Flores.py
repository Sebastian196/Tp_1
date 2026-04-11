import random
import copy
from termcolor import colored
import time

def celdas(conejo, zorro, pasto, dc, dz, dp):
     """
     le asigna de forma aleatoria el valor a una celda

     Args:
        conejo (dict): indicador de un conejo
        zorro (dict): indicador de un zorro
        pasto (str): indicador de pasto pasto
        dc (float): probabilidad de aparición de un conejo
        dz (float): probabilidad de aparición de un zorro
        dp (float): probabilidad de aparición de pasto

     Returns:
        dict, str o None: un animal, la cadena de pasto o None si la celda queda vacía
     """
     prob = random.random() #genero un número random
     if prob <= dc: 
         return copy.deepcopy(conejo)
     elif dc < prob <= (dc + dz): 
         return copy.deepcopy(zorro)
     elif (dc + dz) < prob <= (dc + dz + dp): 
         return pasto
     else:
         return None

def busqueda_de_cordenadas(valor, cordenada_actual, mapa_cordenadas):
     """
      clasifia las codenadas por tipo de elemento dentro de un diccionario(mapa_cordenadas)

     Args:
        valor (dict, str o None): el contenido de la celda
        cordenada_actual (tuple): ubicación (x, y) que representa la ubicación en la matríz
        mapa_cordenadas (dict): diccionario de sets que organiza las posiciones por tipo de elemento.
     """
     if valor is None:
         mapa_cordenadas["vacio"].add(cordenada_actual)
     elif valor == "pasto":
         mapa_cordenadas["pasto"].add(cordenada_actual)
     else:
         tipo_de_animal = valor['tipo']
         if tipo_de_animal == "conejo":
            mapa_cordenadas["conejo"].add(cordenada_actual)
         elif tipo_de_animal == "zorro":
            mapa_cordenadas["zorro"].add(cordenada_actual)

def crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto, dc, dz, dp):
     """
     crea la matriz y asigna un valor a los elementos(utilizando al función celda())

     Args:
        N (int): tamaño de la matríz
        mapa_cordenadas (dict): estructura para registrar las posiciones iniciales
        conejo, zorro, pasto: elementos con los que poblar la matríz
        dc, dz, dp (float): densidades para la generación aleatoria

     Returns:
        list: una matriz de listas representando el ecosistema
     """
     matriz = []
     for fila in range(N):
        matriz.append([]) 
        for columna in range(N): 
            valor = celdas(conejo, zorro, pasto, dc, dz, dp) 
            matriz[fila].append(valor) #le asigno un valor a las celdas utilizando la funcion celdas()
            cordenada_actual = (fila, columna)
            busqueda_de_cordenadas(valor, cordenada_actual, mapa_cordenadas) #a medida que creo la matríz asigno la cordenada
            #(dependiendo de su tipo) a mi diccionario
     return matriz

def obtener_coordenadas_vecinas(x, y, N):
     """
     Identifica las coordenadas vecinas(adyacentes)
     
     Args:
        x (int): fila actual
        y (int): columna actual.
        N (int): tamaño de la matriz para validar los límites.

     Returns:
        list: lista de tuplas con las coordenadas vecinas válidas
     """
     coordenadas_validas = []
     direciones_a_revisar = [(-1,0), (1,0), (0,-1), (0,1)]
     for difx, dify in direciones_a_revisar:
         x_a_revisar = x + difx
         y_a_revisar = y + dify
         if 0 <= x_a_revisar < N and 0 <= y_a_revisar < N: #me aseguro de que la cordenada este dentro de la matríz creada
             coordenadas_validas.append((x_a_revisar, y_a_revisar))
     return coordenadas_validas

def extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp):
     """
     se encarga del cremiento del pasto a lo largo de la simulación

     Args:
        N (int): tamaño de la matriz
        copia_matriz (list): snapshot del turno anterior para consultar estados
        matriz (list): matríz actual donde se aplican los cambios
        mapa_cordenadas (dict): registro de posiciones para actualizar celdas vacías y de pasto
        pasto (str): identificador de pasto
        pp (float): probabilidad de expansión del pasto
     """
     celdas_vacias = list(mapa_cordenadas["vacio"])
     for x, y in celdas_vacias:
         pasto_cercano = False
         coordenadas_vecinas = obtener_coordenadas_vecinas(x, y, N)
         for vx, vy in coordenadas_vecinas:
             if copia_matriz[vx][vy] == pasto:
                 pasto_cercano = True
                 break 
                
         if pasto_cercano:
             prob = random.random()
             if prob <= pp:
                 matriz[x][y] = pasto
                 #actualizo el diccionario de cordenadas
                 mapa_cordenadas["pasto"].add((x, y)) 
                 mapa_cordenadas["vacio"].remove((x, y))

def movimiento_animales(tipo_animal, energia_a_restar, destino_posible1, destino_posible2, matriz, mapa_cordenadas, N, pasto, ganancia_energia, cant_muertes, edad_muertes, copia_matriz):
    """
    controla el movimiento de los animales, el gasto de energía, la alimentación y el registro de muertes

    Args:
        tipo_animal (str): "conejos" o "zorros"
        energia_a_restar (int): costo energético cuando se mueve
        matriz (list): matríz donde se efectúa el movimiento
        cant_muertes (dict): contador de muertes por especie
        edad_muertes (dict): lista de edades al morir
        copia_matriz (list): referencia estática del turno para tomar decisiones de movimiento.
    """
    lista_animal = list(mapa_cordenadas[tipo_animal])
    
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        if animal is None or animal == pasto or animal.get("tipo") != tipo_animal: 
            mapa_cordenadas[tipo_animal].discard((x, y))
            continue
            
        animal["origen"] = (x, y) 
        animal["energia"] -= energia_a_restar 
        animal["edad"] += 1 
        
        #analizo el caso de muerte
        if animal["energia"] <= 0:
            matriz[x][y] = None
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas["vacio"].add((x, y))
            
            tipo_actual = animal["tipo"]
            edad_muertes[tipo_actual].append(animal["edad"])
            cant_muertes[tipo_actual] += 1
            continue

        vecinos_posibles = [] 
        coordenadas_vecinas = obtener_coordenadas_vecinas(x, y, N)
        
        for nx, ny in coordenadas_vecinas:
            celda_vecina_copia = copia_matriz[nx][ny]
            
            es_vacio = (celda_vecina_copia is None)
            es_pasto = (celda_vecina_copia == pasto)
            
            es_conejo = (celda_vecina_copia is not None and celda_vecina_copia != pasto and celda_vecina_copia.get("tipo") == "conejo")#agrego este filtro de seguridad porque antes me daba error
             
            if (destino_posible1 == pasto or destino_posible2 == pasto) and es_pasto:
                vecinos_posibles.append((nx, ny))
            elif (destino_posible1 is None or destino_posible2 is None) and es_vacio:
                vecinos_posibles.append((nx, ny))
            elif tipo_animal == "zorro" and es_conejo:
                vecinos_posibles.append((nx, ny))

        if len(vecinos_posibles) > 0:
            nuevoX, nuevoY = random.choice(vecinos_posibles)
            
            celda_destino = matriz[nuevoX][nuevoY]
            
            if celda_destino is not None and celda_destino != pasto:
                if tipo_animal == "conejo" and celda_destino.get("tipo") == "zorro":
                    celda_destino["energia"] += ganancia_energia
                    cant_muertes["conejo"] += 1
                    edad_muertes["conejo"].append(animal["edad"])
                    matriz[x][y] = None
                    mapa_cordenadas[tipo_animal].discard((x, y))
                    mapa_cordenadas["vacio"].add((x, y))
                    continue 
                elif celda_destino.get("tipo") == tipo_animal:
                    continue 

            #caso en el que un zorro se come a un conejo
            if tipo_animal == "zorro" and celda_destino is not None and celda_destino != pasto and celda_destino.get("tipo") == "conejo":
                cant_muertes["conejo"] += 1
                edad_muertes["conejo"].append(celda_destino["edad"])
                mapa_cordenadas["conejo"].discard((nuevoX, nuevoY))
                animal["energia"] += ganancia_energia
            
            
            if (nuevoX, nuevoY) in mapa_cordenadas["pasto"]:
                mapa_cordenadas["pasto"].discard((nuevoX, nuevoY))
                if tipo_animal == "conejo": 
                    animal["energia"] += ganancia_energia
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["vacio"]:
                mapa_cordenadas["vacio"].discard((nuevoX, nuevoY))

         
            matriz[nuevoX][nuevoY] = animal 
            matriz[x][y] = None
            
            #actualizacio el diccionario de coordenadas
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas[tipo_animal].add((nuevoX, nuevoY)) 
            mapa_cordenadas["vacio"].add((x, y))

def reproduccion_animales(tipo_animal, prob_repro, energia_minima, energia_hijo, matriz, mapa_cordenadas, N):
    """
     reproduce animales

     Args:
        tipo_animal (str): animal que intenta reproducirse
        prob_repro (float): probabilidad de reproducirse
        energia_minima (int): energía requerida para reproducirse
        energia_hijo (int): energía inicial que tendrá el "hijo"
        matriz (list): Matriz principal(represnta el ecosistema)
        mapa_cordenadas (dict): registro de posiciones para ubicar al nuevo animal.
     """
    lista_animal = list(mapa_cordenadas[tipo_animal])
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        if animal is None or type(animal) != dict:
            continue
            
        if animal["energia"] >= energia_minima:
            if random.random() <= prob_repro:
                origen = animal.get("origen")
                if origen:
                    hx, hy = origen
                    # Verificamos si la celda de origen realmente quedó vacía
                    if (hx, hy) in mapa_cordenadas["vacio"]:
                        nuevo_animal = copy.deepcopy(animal)
                        nuevo_animal["energia"] = energia_hijo 
                        nuevo_animal["edad"] = 0 
                        
                        matriz[hx][hy] = nuevo_animal
                        mapa_cordenadas[tipo_animal].add((hx, hy))
                        mapa_cordenadas["vacio"].discard((hx, hy))

def imprimir_matriz(N, matriz, mapa_cordenadas, turno):
    """
    se imprime la matríz en la terminal

    Args:
        N (int): tamaño de la matríz
        matriz (list): matríz actual
        mapa_cordenadas (dict): diccionario para contar animales vivos de forma eficiente
        turno (int): número turnos efectuados 
    """
    conejos_vivos = len(mapa_cordenadas["conejo"])
    zorros_vivos = len(mapa_cordenadas["zorro"])
    
    print("-------------------------")
    print(f"Turno: {turno+1} 🐇Conejos: {conejos_vivos} 🦊Zorros: {zorros_vivos}")
    print("-------------------------")
    
    for fila in range(N):
        for columna in range(N):
            if matriz[fila][columna] is None:
                print("  ", end=" ")
            elif matriz[fila][columna] == 'pasto':
                print(colored("▓▓", "green"), end=" ")
            elif matriz[fila][columna]['tipo'] == 'conejo':
                print(colored("▓▓", "cyan"), end=" ")
            elif matriz[fila][columna]['tipo'] == 'zorro':
                print(colored("▓▓", "red"), end=" ")
        print() 
    time.sleep(0.1)

def snapshot(matriz):
    """
    creo el snapshot

    Args:
        matriz (list): La grilla original a copiar.

    Returns:
        list: una copia independiente de toda la estructura de la matriz.
    """
    return copy.deepcopy(matriz)
    """
    creo el snapshot

    Args:
        matriz (list): La grilla original a copiar.

    Returns:
        list: una copia independiente de toda la estructura de la matriz.
    """
    return copy.deepcopy(matriz)