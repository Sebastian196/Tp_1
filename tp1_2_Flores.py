from tp1_funciones_Flores import crear_matriz, imprimir_matriz, extension_pasto, movimiento_animales, reproduccion_animales, snapshot


N = 25 # matriz = NxN
dc = 0.12 # densidad inicial de conejos
dz = 0.20 # densidad inicial de zorros
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
    'tipo': 'conejo',
    'energia': ec,
    'edad': 0
}
zorro = {
    'tipo': 'zorro',
    'energia': ez,
    'edad': 0
}

pasto = 'pasto'

cant_muertes = {
    "conejo": 0,
    "zorro": 0,
}

edad_muertes = {
    "conejo": [],
    "zorro": [],
}

for simulacion in range(100):
    mapa_cordenadas = {
        "conejo": set(),
        "zorro": set(),
        "pasto": set(),
        "vacio": set()
    }
    
    matriz = crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto, dc, dz, dp)
    
    for turno in range(tmax):
        copia_matriz = snapshot(matriz)
        
        extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp)
        
        movimiento_animales("zorro", 2, None, pasto, matriz, mapa_cordenadas, N, pasto, gz, cant_muertes, edad_muertes, copia_matriz)
        movimiento_animales("conejo", 1, None, pasto, matriz, mapa_cordenadas, N, pasto, gc, cant_muertes, edad_muertes, copia_matriz)
        
        reproduccion_animales("conejo", prc, emin, ec, matriz, mapa_cordenadas, N)
        reproduccion_animales("zorro", prz, emin, ez, matriz, mapa_cordenadas, N)
        
        if len(mapa_cordenadas["conejo"]) == 0 or len(mapa_cordenadas["zorro"]) == 0:
            break

edades_conejos = sum(edad_muertes["conejo"])
edades_zorros = sum(edad_muertes["zorro"])

total_muertes_conejos = cant_muertes["conejo"]
total_muertes_zorros = cant_muertes["zorro"]

esperanza_conejo = edades_conejos / total_muertes_conejos if total_muertes_conejos > 0 else 0
esperanza_zorro = edades_zorros / total_muertes_zorros if total_muertes_zorros > 0 else 0

print(f"Muertes registradas - Conejos: {total_muertes_conejos} | Zorros: {total_muertes_zorros}")
print(f"Esperanza de vida del conejo: {esperanza_conejo:.2f} turnos")
print(f"Esperanza de vida del zorro: {esperanza_zorro:.2f} turnos")