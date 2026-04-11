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

simulaciones_a_realizar = 50 

#encabezado de la tabla
print("+--------+---------------------+")
print("| d_z    | Sin extinciones     |")
print("+--------+---------------------+")

for paso in range(20):
    dz = round(0.01 + paso * 0.02, 2)
    num_extinciones = 0 
    
    for i in range(simulaciones_a_realizar): 
        mapa_cordenadas = {
            "conejo" : set(), 
            "zorro" : set(), 
            "pasto" : set(), 
            "vacio" : set()
        }
        cant_muertes = {
            "conejo": 0, 
            "zorro": 0
        }
        edad_muertes = {
            "conejo": [], 
            "zorro": []
        }
        matriz = crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto, dc, dz, dp)
        
        for turno in range(tmax):
            copia_matriz = snapshot(matriz)
            
            extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp)
            
            movimiento_animales("conejo", 1, None, pasto, matriz, mapa_cordenadas, N, pasto, gc, cant_muertes, edad_muertes, copia_matriz)
            movimiento_animales("zorro", 2, None, pasto, matriz, mapa_cordenadas, N, pasto, gz, cant_muertes, edad_muertes, copia_matriz)
    
            reproduccion_animales("conejo", prc, emin, ec, matriz, mapa_cordenadas, N)
            reproduccion_animales("zorro", prz, emin, ez, matriz, mapa_cordenadas, N)
            
            #caso de exitinción de una especie
            if len(mapa_cordenadas["conejo"]) == 0 or len(mapa_cordenadas["zorro"]) == 0:
                num_extinciones += 1
                break
    
    porcentaje_sin_extincion = 100.0 - ((num_extinciones * 100.0) / simulaciones_a_realizar)
    
    print(f"| {dz:.2f}   | {porcentaje_sin_extincion:>7.2f} %           |") 
    print("+--------+---------------------+")