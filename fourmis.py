import numpy as np

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)))

def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 

RANOMSEED = 12345

NBFOURMIS = 100
NBEPOCHS = 500
NBVILLES = len(_CITIES)
ALPHA = 0.6
BETA = 0.4
EVAPORATION = 0.8
COEFFEXPLORATION = 0.05
Q = 1 / NBVILLES

distances = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
pheromones = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)

for i in range(NBVILLES):
    for j in range(NBVILLES):
        distances[i,j] = distance(_CITIES[i][1], _CITIES[j][1])

def goAnt():
    # Retourne le chemin et le cout total trouvé par une fourmi sur son tour
    # Tous les chemins partent de 0
    return [], 0 # TODO

# Ici tout est pret

for epoch in range(NBEPOCHS):
    pherobis = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
    for fourmi in range(NBFOURMIS):
        chemin, longueur = goAnt()
        assert longueur > 0
        deposePhero = Q / longueur 
        ancienneVille = 0
        for ville in chemin:
            pherobis[ancienneVille, ville] += deposePhero
            ancienneVille = ville

    pheromones *= EVAPORATION
    pheromones += pherobis

