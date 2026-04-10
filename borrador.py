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