from tp1_funciones_Flores import crear_matriz, imprimir_matriz, extension_pasto, movimiento_animales, reproduccion_animales, snapshot

N = 25 # matriz = NxN
dc = 0.12 # densidad inicial de conejos
dp = 0.35 # densidad inicial de pasto
ec = 5 # energia inicial de los conejos
ez = 12 # energia inicial de los zorros
gc = 4 # energia que gana un conejo al comer pasto
gz = 8 # energia que gana un zorro al comer un conejo
pp = 0.50 # probabilidad de que en un turno el pasto crezca en una celda vacia adyacente
prc = 0.18 # prob de que un conejo se reproduzca (si tiene energ suficiente)
prz = 0.18 # prob  de que un zorro se reproduzca
emin = 4 # eng necesaia para que un animal pueda reproducirse
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

cant_muertes = {
    "conejo": cant_muertes_conejos,
    "zorro": cant_muertes_zorros,
}

edad_muertes = {
    "conejo" : edad_muerte_conejos,
    "zorro": edad_muerte_zorros,
}



if animal["energia"] == 0:
    edad_muertes[animal].append(animal[edad])
    cant_muertes[animal] +=1
    
    
    
dz = 0.20 # densidad inicial de zorros

dz = 0.01
simulaciones_a_realizar = 50 


matriz = crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto)


while dz < 0.39:
    num_extinciones = 0 
    for i in range(simulaciones_a_realizar): 
        copia_matriz = snapshot(matriz)
        
     #Realizo la simulación
        movimiento_animales("conejos", 1, None, pasto, matriz, mapa_cordenadas, N, pasto, gc, cant_muertes, edad_muertes)
        movimiento_animales("zorros", 2, None, pasto, matriz, mapa_cordenadas, N, pasto, gz, cant_muertes, edad_muertes)
        
        reproduccion_animales("conejos", prc, emin, ec, matriz, mapa_cordenadas, N)
        reproduccion_animales("zorros", prz, emin, ez, matriz, mapa_cordenadas, N)
        
        extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp)
        
        # Evalúa la condición de fin de simulación
        if len(mapa_cordenadas["conejos"]) == 0 or len(mapa_cordenadas["zorros"]) == 0:
            num_extinciones += 1
    
    porcentaje_extinción = (num_extinciones * 100)/simulaciones_a_realizar
    print(porcentaje_extinción)
    dz += 0.02