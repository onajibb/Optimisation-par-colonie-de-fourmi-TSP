import numpy as np

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)))


# Bordeaux est le point de départ
# Définir comment on va définir la présence ou non de nourriture 
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

# définir la ville de départ 


for i in range(NBVILLES):
    for j in range(NBVILLES):
        distances[i,j] = distance(_CITIES[i][1], _CITIES[j][1])

#encodage ville -> nombre 

list_villes = np.arange(len(_CITIES))
noms_villes = np.asarray(_CITIES)[:,0]

correspondancies = list(zip(list_villes, noms_villes))

clas

def goAnt():
    # Retourne le chemin et le cout total trouvé par une fourmi sur son tour
    # Tous les chemins partent de 0
    # 0 est bordeaux 
    chemin = []
    pos_init = 0
  # la fourmi se trouve dans la ville de Bordeaux au début 
    pos = pos_init
    # choisir le chemin de départ
    time = 0
    while(1): #condition la fourmi doit retourner chez elle 
        # position de la fourmi
        if(pos == pos_init):
            break 
        
        ville_visite = chemin[:,0] #index des villes #chemin = matrix Mx2 C1 = index de la ville C2 = distance parcouru pour arriver à la ville   
        
        #vérifie si la ville n'est pas déjà visitée    
        villes_potentiels = [[i,distances[i, pos]]for i in range(len(D)) if i not in villes_visites ]
        probabilite = np.zeros((2, len(villes_potentiels)))
        for i in range(len(ville_potentiels)): 
            index_ville = ville_potentiels[i][0]
            probabilite[0,i] = (((pheromones[villes_potentiels[i][0],pos])**(alpha)) * ((1/distances[villes_potentiels[i][0],pos])**(beta)))/np.sum((pheromones[villes_potentiels[i][0],pos])**(alpha) * ((1/distances[villes_potentiels[i][0],pos])**(beta)))  
            probabilite[1,i] = villes_potentiels[i][0]
        #mettre à jour la matrice des pheromones

        if(time == 0):
            probabilite[0,pos] = 0 
        
        ville_to_visit = np.argmax(probabilite[0,:])
        index_ville_to_visit = probabilite[1, ville_to_visit]

        #voir si la ville a déjà été visitée
        
        else: 
            chemin.append([distance[index_ville_to_visit, pos] ,pos])

        pos = index_ville_to_visit

    #retourne le chemin
    return chemin # TODO

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

