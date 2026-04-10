import random
import copy
from termcolor import colored
import time

N = 25 # matriz = NxN
dc = 0.12 #densidad inicial de conejos
dz = 0.20 #densidad inicial de zorros
dp = 0.35 #denisdad inicial de pasto
ec = 5 #energia inicial de los conejos
ez = 12 #energia inicial de los zorros
gc = 4 #energia que gana un conejo al comer pasto
gz = 8 #energia que gana un zorro al comer un conejo
pp= 0.50 #probabilidad de que en un turno el pasto crezca en una celda vacia adyacente
prc = 0.18 #prob de que un conejo se reproduzca(si tiene energ suficiente)
prz = 0.18 #prob  de que un zorro se reproduzca
emin = 4 #eng necesaia para que un animal pueda reproducirse
tmax = 200


conejo = {
    'tipo' : 'conejo',
    'energia': ec,
    'edad': 0
}
zorro = {
    'tipo' : 'zorro',
    'energia': ez,
    'edad': 0
}

pasto = 'pasto'

mapa_cordenadas = {
    "conejos" : set(),
    "zorros" : set(),
    "pasto" : set(),
    "vacio" : set()
}

def celdas():
    prob = random.random()
    if prob <= 0.12: #conejo
        return copy.deepcopy(conejo)
    elif 0.12 < prob <= 0.32: #zorro
        return copy.deepcopy(zorro)
    elif 0.32 < prob <= 0.67: #pasto
        return pasto
    else:
        return None   
    """
    Con esta función le asigno un valor a las diferentes celdas basado en las porbabilidades del enunciado
    """

def crear_matriz(N):
    matriz = []
    for fila in range(N):
        matriz.append([]) #creo una fila
        for columna in range(N): 
            valor = celdas() #variable temporal que tome un valor como los del enunciado
            matriz[fila].append(valor) #agregar ese valor a la fila que creada en el paso enterior
            cordenada_actual = (fila, columna)
            busqueda_de_cordenadas(valor, cordenada_actual)
    return matriz
    """
    Esta función genera las filas y columnas de la matríz de NxN y, ademas, almacena las cordenadas de los diferentes
    tipos de celdas
    """

    """ cordenada_actual = (fila, columna) #Almaceno temporalmente las "cordenadas"[fila, columna]
            busqueda_de_cordenadas(valor, cordenada_actual)
    """
    
def busqueda_de_cordenadas(valor, cordenada_actual):
    if valor == None:
        mapa_cordenadas["vacio"].add(cordenada_actual)
    elif valor == "pasto":
        mapa_cordenadas["pasto"].add(cordenada_actual)
    else:
        # Si no es None ni pasto, es un animal. Miramos su 'tipo'
        tipo_de_animal = valor['tipo']
        if tipo_de_animal == "conejo":
            mapa_cordenadas["conejos"].add(cordenada_actual)
        elif tipo_de_animal == "zorro":
            mapa_cordenadas["zorros"].add(cordenada_actual)
    """
    Clasifica y guarda una coordenada en el conjunto (set) correspondiente 
    dentro del diccionario mapa_cordenadas.
    """
    
def extension_pasto(N, copia_matriz):
    # Iteramos solo sobre una copia de las celdas vacías actuales
    celdas_vacias = list(mapa_cordenadas["vacio"])
    
    for x, y in celdas_vacias:
        pasto_cercano = False
        coordenadas_vecinas = obtener_cordenadas_vecinas(x, y, N)
        
        # Verificamos si algún vecino tiene pasto en la copia del turno
        # (usamos la copia para evitar que el pasto crezca en cadena en el mismo turno)
        for vx, vy in coordenadas_vecinas:
            if copia_matriz[vx][vy] == pasto:
                pasto_cercano = True
                break # Si ya encontramos pasto, no hace falta seguir mirando vecinos
                
        if pasto_cercano:
            prob = random.random()
            if prob <= pp:
                # Actualizamos la matriz original
                matriz[x][y] = pasto
                
                # Actualizamos los sets de forma eficiente
                mapa_cordenadas["pasto"].add((x, y))
                mapa_cordenadas["vacio"].remove((x, y))

def movimiento_animales(tipo_animal, energia_a_restar, destino_posible1, destino_posible2):
    lista_animal = list(mapa_cordenadas[tipo_animal])
    
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        # Filtro de seguridad: Si el animal ya no existe en la matriz (fue pisado/comido)
        # lo eliminamos del set para limpiar los "fantasmas" y saltamos el turno.
        if animal is None or type(animal) is not dict or animal.get("tipo") != tipo_animal[:-1]:
            mapa_cordenadas[tipo_animal].discard((x, y))
            continue
        
        animal["energia"] -= energia_a_restar 
        animal["edad"] += 1 
        
        if animal["energia"] <= 0:
            matriz[x][y] = None
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas["vacio"].add((x, y))
            continue

        vecinos_posibles = [] 
        cordenadas_vecinas = obtener_cordenadas_vecinas(x, y, N)
        
        for nx, ny in cordenadas_vecinas:
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
            
            # CORRECCIÓN: Limpiar el set de destino SIEMPRE, sin importar qué animal lo pise
            if (nuevoX, nuevoY) in mapa_cordenadas["pasto"]:
                mapa_cordenadas["pasto"].discard((nuevoX, nuevoY))
                if tipo_animal == "conejos": 
                    animal["energia"] += gc
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["conejos"]:
                mapa_cordenadas["conejos"].discard((nuevoX, nuevoY))
                if tipo_animal == "zorros":  
                    animal["energia"] += gz
                    
            elif (nuevoX, nuevoY) in mapa_cordenadas["vacio"]:
                mapa_cordenadas["vacio"].discard((nuevoX, nuevoY))

            # Actualizamos la matriz
            matriz[nuevoX][nuevoY] = animal 
            matriz[x][y] = None
            
            # Actualizamos los sets de ubicación del animal
            mapa_cordenadas[tipo_animal].discard((x, y)) 
            mapa_cordenadas[tipo_animal].add((nuevoX, nuevoY)) 
            mapa_cordenadas["vacio"].add((x, y))

def obtener_cordenadas_vecinas(x, y, N):
    """
    Devuelve una lista con las coordenadas (x, y) de los vecinos
    adyacentes que están dentro de los límites de la matriz.
    """
    cordenadas_validas = []
    direciones_a_revisar = [(-1,0), (1,0), (0,-1), (0,1)]
    
    for difx, dify in direciones_a_revisar:
        x_a_revisar = x + difx
        y_a_revisar = y + dify
        
        #e aseguro de que no se escapen de la matriz
        if 0 <= x_a_revisar < N and 0 <= y_a_revisar < N:
            cordenadas_validas.append((x_a_revisar, y_a_revisar))
            
    return cordenadas_validas

def reproduccion_animales(tipo_animal, prob_repro, energia_minima, energia_hijo):
    lista_animal = list(mapa_cordenadas[tipo_animal])
    
    for x, y in lista_animal:
        animal = matriz[x][y]
        
        if animal is None or type(animal) is not dict:
            continue
            
        if animal["energia"] >= energia_minima:
            if random.random() <= prob_repro:
                vecinos_vacios = []
                cordenadas_vecinas = obtener_cordenadas_vecinas(x, y, N)
                
                # CAMBIO NECESARIO: Verificar vacío consultando el set actualizado
                for nx, ny in cordenadas_vecinas:
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

def imprimir_matriz(N,matriz, turno):
    conejos_vivos = len(mapa_cordenadas["conejos"])
    zorros_vivos = len(mapa_cordenadas["zorros"])
    
    print("-------------------------")
    print(f"Turno: {turno+1} 🐇Conejos: {conejos_vivos} 🦊Zorros: {zorros_vivos}")
    print("-------------------------")
    
    for fila in range(N):
        for columna in range(N):
            if matriz[fila][columna] == None:
                print("  ", end=" ") # Dos espacios para mantener el ancho
            elif matriz[fila][columna] == 'pasto':
                print(colored("▓▓", "green"), end=" ")
            elif matriz[fila][columna]['tipo'] == 'conejo':
                print(colored("▓▓", "cyan"), end=" ")
            elif matriz[fila][columna]['tipo'] == 'zorro':
                print(colored("▓▓", "red"), end=" ")
        print() # Salto de línea al terminar cada fila
    time.sleep(0.1)
    """
    Esta función imprime la matríz y tiene un tiempo de espera para que se pueda
    apreciar la simulación
    """

def snapshot(matriz):
    return copy.deepcopy(matriz)
    """
    Esta función genera una copia de la matríz
    """


matriz = crear_matriz(N)


for turno in range(tmax): 
    imprimir_matriz(N, matriz, turno)
    copia_matriz = snapshot(matriz)
    
    
    movimiento_animales("conejos", 1, None, "pasto" )
    movimiento_animales("zorros", 2, None, "pasto")
    
    reproduccion_animales("conejos", prc, emin, ec)
    reproduccion_animales("zorros", prz, emin, ez)
    
    extension_pasto(N, copia_matriz)
    
    if len(mapa_cordenadas["conejos"]) == 0 or len(mapa_cordenadas["zorros"]) == 0:
        imprimir_matriz(N, matriz, turno)
        break

