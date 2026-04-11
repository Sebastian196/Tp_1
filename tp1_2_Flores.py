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

cant_muertes_conejos = 0
cant_muertes_zorros = 0

edad_muerte_conejos = []
edad_muerte_zorros = []

cant_muertes = {
    "conejo": cant_muertes_conejos,
    "zorro": cant_muertes_zorros,
}

edad_muertes = {
    "conejo" : edad_muerte_conejos,
    "zorro": edad_muerte_zorros,
}

matriz = crear_matriz(N, mapa_cordenadas, conejo, zorro, pasto)
for turnos in range(100):
     copia_matriz = snapshot(matriz)
    
    # Se pasa la matriz, el mapa y las variables que necesitan
     movimiento_animales("conejos", 1, None, pasto, matriz, mapa_cordenadas, N, pasto, gc, cant_muertes, edad_muertes, copia_matriz)
     movimiento_animales("zorros", 2, None, pasto, matriz, mapa_cordenadas, N, pasto, gz, cant_muertes, edad_muertes, copia_matriz)
    
     reproduccion_animales("conejos", prc, emin, ec, matriz, mapa_cordenadas, N)
     reproduccion_animales("zorros", prz, emin, ez, matriz, mapa_cordenadas, N)
    
     extension_pasto(N, copia_matriz, matriz, mapa_cordenadas, pasto, pp)

edades_conejos = sum(edad_muertes["conejo"])
edades_zorros = sum(edad_muertes["zorro"])

total_muertes_conejos = cant_muertes["conejo"]
total_muertes_zorros = cant_muertes["zorro"]

print(f"Muertes regsitradas - Conejos: {total_muertes_conejos} | Zorros: {total_muertes_zorros}")
if total_muertes_conejos > 0:
    esperanza_conejos = edades_conejos / total_muertes_conejos
    print(f"La esperanza de vida de los conejos es: {esperanza_conejos:.2f} turnos")
else:
    print("No hubo muertes de conejos")

if total_muertes_zorros > 0:
    esperanza_zorros = edades_zorros / total_muertes_zorros
    print(f"La esperanza de vida de los zorros es: {esperanza_zorros:.2f} turnos")
else:
    print("No hubieron muertes de zorros")
