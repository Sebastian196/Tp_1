import random
import copy
from termcolor import colored
import time

def celdas(conejo, zorro, pasto, dc, dz, dp):

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
    matriz = []
    for fila in range(N):
        matriz.append([]) 
        for columna in range(N): 
            valor = celdas(conejo, zorro, pasto, dc, dz, dp) 
            matriz[fila].append(valor) #le asigno un valor a las celdas utilizando la funcion celdas()
            cordenada_actual = (fila, columna)
            busqueda_de_cordenadas(valor, cordenada_actual, mapa_cordenadas) #a medida que 
    return matriz

def obtener_coordenadas_vecinas(x, y, N):
    coordenadas_validas = []
    direciones_a_revisar = [(-1,0), (1,0), (0,-1), (0,1)]
    for difx, dify in direciones_a_revisar:
        x_a_revisar = x + difx
        y_a_revisar = y + dify
        if 0 <= x_a_revisar < N and 0 <= y_a_revisar < N: #me aseguro de que la cordenada este dentro de la matríz creada
            coordenadas_validas.append((x_a_revisar, y_a_revisar))
    return coordenadas_validas

def extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp):
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
                mapa_cordenadas["pasto"].add((x, y))
                mapa_cordenadas["vacio"].remove((x, y))

def movimiento_animales(tipo_animal, energia_a_restar, destino_posible1, destino_posible2, matriz, mapa_cordenadas, N, pasto, ganancia_energia, cant_muertes, edad_muertes, copia_matriz):
    lista_animal = list(mapa_cordenadas[tipo_animal])
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        if animal is None or type(animal) is not dict or animal.get("tipo") != tipo_animal[:-1]:
            mapa_cordenadas[tipo_animal].discard((x, y))
            continue
            
        animal["origen"] = (x, y) # Guardamos el origen para la etapa de reproducción
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
        
        # Evaluar decisiones mirando ÚNICAMENTE el snapshot (copia_matriz)
        for nx, ny in coordenadas_vecinas:
            elemento_snap = copia_matriz[nx][ny]
            es_vacio = elemento_snap is None
            es_pasto = elemento_snap == pasto
            es_conejo = type(elemento_snap) is dict and elemento_snap.get("tipo") == "conejo"
             
            if (destino_posible1 == pasto or destino_posible2 == pasto) and es_pasto:
                vecinos_posibles.append((nx, ny))
            elif (destino_posible1 is None or destino_posible2 is None) and es_vacio:
                vecinos_posibles.append((nx, ny))
            elif tipo_animal == "zorros" and es_conejo:
                vecinos_posibles.append((nx, ny))

        if len(vecinos_posibles) > 0:
            nuevoX, nuevoY = random.choice(vecinos_posibles)
            
            ocupante_actual = matriz[nuevoX][nuevoY]
            
            # Evitar colisiones en la grilla que se está construyendo
            if ocupante_actual is not None and ocupante_actual != pasto:
                if tipo_animal == "conejos" and type(ocupante_actual) is dict and ocupante_actual.get("tipo") == "zorro":
                    # El conejo se movió a donde ya había llegado un zorro
                    ocupante_actual["energia"] += ganancia_energia
                    cant_muertes["conejo"] += 1
                    edad_muertes["conejo"].append(animal["edad"])
                    matriz[x][y] = None
                    mapa_cordenadas[tipo_animal].discard((x, y))
                    mapa_cordenadas["vacio"].add((x, y))
                    continue 
                elif type(ocupante_actual) is dict and ocupante_actual.get("tipo") == tipo_animal[:-1]:
                    continue # Ya hay un animal de mi misma especie que llegó antes, me quedo en origen

            # Zorro comiendo conejo en su lugar de origen
            if tipo_animal == "zorros" and type(ocupante_actual) is dict and ocupante_actual.get("tipo") == "conejo":
                cant_muertes["conejo"] += 1
                edad_muertes["conejo"].append(ocupante_actual["edad"])
                mapa_cordenadas["conejos"].discard((nuevoX, nuevoY))
                animal["energia"] += ganancia_energia
            
            # Lógica normal de limpieza en el mapa de coordenadas
            if (nuevoX, nuevoY) in mapa_cordenadas["pasto"]:
                mapa_cordenadas["pasto"].discard((nuevoX, nuevoY))
                if tipo_animal == "conejos": 
                    animal["energia"] += ganancia_energia
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["vacio"]:
                mapa_cordenadas["vacio"].discard((nuevoX, nuevoY))

            matriz[nuevoX][nuevoY] = animal 
            matriz[x][y] = None
            
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas[tipo_animal].add((nuevoX, nuevoY)) 
            mapa_cordenadas["vacio"].add((x, y))

def reproduccion_animales(tipo_animal, prob_repro, energia_minima, energia_hijo, matriz, mapa_cordenadas, N):
    lista_animal = list(mapa_cordenadas[tipo_animal])
    for x, y in lista_animal:
        animal = matriz[x][y]
        if animal is None or type(animal) is not dict:
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
    return copy.deepcopy(matriz)