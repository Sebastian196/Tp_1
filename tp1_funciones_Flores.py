import random
import copy
from termcolor import colored
import time

def celdas(conejo, zorro, pasto):
    prob = random.random()
    if prob <= 0.12: #conejo
        return copy.deepcopy(conejo)
    elif 0.12 < prob <= 0.32: #zorro
        return copy.deepcopy(zorro)
    elif 0.32 < prob <= 0.67: #pasto
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

def crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto):
    matriz = []
    for fila in range(N):
        matriz.append([]) 
        for columna in range(N): 
            valor = celdas(conejo, zorro, pasto) 
            matriz[fila].append(valor) 
            cordenada_actual = (fila, columna)
            busqueda_de_cordenadas(valor, cordenada_actual, mapa_cordenadas)
    return matriz

def obtener_coordenadas_vecinas(x, y, N):
    coordenadas_validas = []
    direciones_a_revisar = [(-1,0), (1,0), (0,-1), (0,1)]
    for difx, dify in direciones_a_revisar:
        x_a_revisar = x + difx
        y_a_revisar = y + dify
        if 0 <= x_a_revisar < N and 0 <= y_a_revisar < N:
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

def movimiento_animales(tipo_animal, energia_a_restar, destino_posible1, destino_posible2, matriz, mapa_cordenadas, N, pasto, ganancia_energia):
    lista_animal = list(mapa_cordenadas[tipo_animal])
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        if animal is None or type(animal) is not dict or animal.get("tipo") != tipo_animal[:-1]:
            mapa_cordenadas[tipo_animal].discard((x, y))
            continue
        
        animal["energia"] -= energia_a_restar 
        animal["edad"] += 1 
        
        #analizo el caso de la muerte del animal
        if animal["energia"] <= 0:
            matriz[x][y] = None
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas["vacio"].add((x, y))
            edad_muertes[animal].append(animal[edad])
            cant_muertes[animal] +=1
            continue

        vecinos_posibles = [] 
        coordenadas_vecinas = obtener_coordenadas_vecinas(x, y, N)
        
        for nx, ny in coordenadas_vecinas:
            es_vacio = (nx, ny) in mapa_cordenadas["vacio"]
            es_pasto = (nx, ny) in mapa_cordenadas["pasto"]
            es_conejo = (nx, ny) in mapa_cordenadas["conejos"]
             
            if (destino_posible1 == pasto or destino_posible2 == pasto) and es_pasto:
                vecinos_posibles.append((nx, ny))
            elif (destino_posible1 is None or destino_posible2 is None) and es_vacio:
                vecinos_posibles.append((nx, ny))
            elif tipo_animal == "zorros" and es_conejo:
                vecinos_posibles.append((nx, ny))

        if len(vecinos_posibles) > 0:
            nuevoX, nuevoY = random.choice(vecinos_posibles)
            
            if (nuevoX, nuevoY) in mapa_cordenadas["pasto"]:
                mapa_cordenadas["pasto"].discard((nuevoX, nuevoY))
                if tipo_animal == "conejos": 
                    animal["energia"] += ganancia_energia
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["conejos"]:
                mapa_cordenadas["conejos"].discard((nuevoX, nuevoY))
                if tipo_animal == "zorros":  
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
                vecinos_vacios = []
                coordenadas_vecinas = obtener_coordenadas_vecinas(x, y, N)
                for nx, ny in coordenadas_vecinas:
                    if (nx, ny) in mapa_cordenadas["vacio"]:
                        vecinos_vacios.append((nx, ny))
                        
                if len(vecinos_vacios) > 0:
                    hijoX, hijoY = random.choice(vecinos_vacios)
                    nuevo_animal = copy.deepcopy(animal)
                    nuevo_animal["energia"] = energia_hijo 
                    nuevo_animal["edad"] = 0 
                    
                    matriz[hijoX][hijoY] = nuevo_animal
                    mapa_cordenadas[tipo_animal].add((hijoX, hijoY))
                    mapa_cordenadas["vacio"].discard((hijoX, hijoY))

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