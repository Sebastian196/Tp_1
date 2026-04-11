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
            mapa_cordenadas["conejos"].add(cordenada_actual)
         elif tipo_de_animal == "zorro":
            mapa_cordenadas["zorros"].add(cordenada_actual)

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
                
         if pasto_cercano == True:
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
        
        # El parámetro tipo_animal viene en plural ("conejos", "zorros").
        # Usamos el slicing [:-1] para borrar la última letra (la "s") y obtener el singular ("conejo", "zorro")
        # Esto permite compararlo correctamente con el valor guardado en el diccionario bajo la clave "tipo".
        if animal == None or animal == pasto or animal.get("tipo") != tipo_animal[:-1]: #tengo que usar slicing para tener el tipo de forma correcta
            mapa_cordenadas[tipo_animal].discard((x, y))
            continue
            
        animal["origen"] = (x, y) 
        animal["energia"] -= energia_a_restar 
        animal["edad"] += 1 
        
        # Analizo el caso de muerte por energía
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
            # Consultamos la copia estática del inicio del turno
            celda_vecina_copia = copia_matriz[nx][ny]
            
            es_vacio = (celda_vecina_copia == None)
            es_pasto = (celda_vecina_copia == pasto)
            
            # Verificación en cascada: asegura que no sea vacío, ni pasto, antes de usar .get()
            es_conejo = (celda_vecina_copia != None and celda_vecina_copia != pasto and celda_vecina_copia.get("tipo") == "conejo")
             
            if (destino_posible1 == pasto or destino_posible2 == pasto) and es_pasto == True:
                vecinos_posibles.append((nx, ny))
            elif (destino_posible1 == None or destino_posible2 == None) and es_vacio == True:
                vecinos_posibles.append((nx, ny))
            elif tipo_animal == "zorros" and es_conejo == True:
                vecinos_posibles.append((nx, ny))

        if len(vecinos_posibles) > 0:
            nuevoX, nuevoY = random.choice(vecinos_posibles)
            
            # Consultamos el estado actual y real de la matriz en la coordenada elegida
            celda_destino = matriz[nuevoX][nuevoY]
            
            if celda_destino != None and celda_destino != pasto:
                # Si soy un conejo y me muevo a donde justo acaba de llegar un zorro
                if tipo_animal == "conejos" and celda_destino.get("tipo") == "zorro":
                    celda_destino["energia"] += ganancia_energia
                    cant_muertes["conejo"] += 1
                    edad_muertes["conejo"].append(animal["edad"])
                    matriz[x][y] = None
                    mapa_cordenadas[tipo_animal].discard((x, y))
                    mapa_cordenadas["vacio"].add((x, y))
                    continue 
                # Si en el destino ya se ubicó un animal de mi misma especie
                elif celda_destino.get("tipo") == tipo_animal[:-1]:
                    continue # El lugar está ocupado por un aliado, el movimiento se cancela y me quedo en origen

            # Zorro comiendo conejo en la matriz real
            if tipo_animal == "zorros" and celda_destino != None and celda_destino != pasto and celda_destino.get("tipo") == "conejo":
                cant_muertes["conejo"] += 1
                edad_muertes["conejo"].append(celda_destino["edad"])
                mapa_cordenadas["conejos"].discard((nuevoX, nuevoY))
                animal["energia"] += ganancia_energia
            
            # Lógica normal de limpieza en el mapa de coordenadas para pasto y vacío
            if (nuevoX, nuevoY) in mapa_cordenadas["pasto"]:
                mapa_cordenadas["pasto"].discard((nuevoX, nuevoY))
                if tipo_animal == "conejos": 
                    animal["energia"] += ganancia_energia
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["vacio"]:
                mapa_cordenadas["vacio"].discard((nuevoX, nuevoY))

            # Ejecución final del movimiento
            matriz[nuevoX][nuevoY] = animal 
            matriz[x][y] = None
            
            # Actualización del registro de coordenadas
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
    conejos_vivos = len(mapa_cordenadas["conejos"])
    zorros_vivos = len(mapa_cordenadas["zorros"])
    
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