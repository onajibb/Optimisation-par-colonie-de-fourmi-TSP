import numpy as np
from itertools import combinations
import time
import random
# https://github.com/Akavall/AntColonyOptimization/blob/master/ant_colony.py

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)))


_NEST = 0
_SEARCHING_PATH = 1
_RETURNING_NEST = 2
_CITY_NID = 'Bordeaux'
_CITY_FOOD = 'Caen'

#encodage ville -> nombre 

list_villes = list(np.arange(len(_CITIES)))
noms_villes = [list(_CITIES)[i][0] for i in range(len(_CITIES))]

dict_cities = dict(zip(list_villes, noms_villes))

# Bordeaux est le point de départ
# Définir comment on va définir la présence ou non de nourriture 
def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 


RANOMSEED = 12345

NBFOURMIS = 100
NBEPOCHS = 500
NBVILLES = len(_CITIES)
ALPHA = 0.5
BETA = 0.5
EVAPORATION = 0.8
COEFFEXPLORATION = 0.05
Q = 1 / NBVILLES

distances = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
pheromones = 0.01 + np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
visibility = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
# définir la ville de départ 
print(dict_cities)

for i in range(NBVILLES):
    for j in range(NBVILLES):
        distances[i,j] = distance(_CITIES[i][1], _CITIES[j][1])
        if(i!=j): 
            visibility[i,j] = 1/distances[i,j]
        else: 
            visibility[i,j] = 0


def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

def op(tau, eta): 
    return tau**(ALPHA) * eta**(BETA)


class Fourmi(): 
    def __init__(self,visited_cities, pheromones, visibility):
        # les villes visités par la fourmi et le chemin de la fourmi
        self.visited_cities = visited_cities
        inter = self.visited_cities
        self.to_visit=[]
        random_number = random.random()
        for ville in noms_villes:
            if(ville not in self.visited_cities):
                self.to_visit.append(ville)
        # la ville visité par la fourmi
        self.current_visited_city = self.visited_cities[-1]
        # la ville à visiter par la fourmi
        self.current_city_to_visit = None
        # la distance totale parcouru 
        self.path_length = 0
        self.path_length = self.calculate_path_length()
        # état de la fourmi
        self.state = None
        self.get_state()
        self.time = 0 


    def get_state(self): 
        if(self.current_visited_city == "Bordeaux"):
            self.state = _NEST
        elif(self.current_visited_city == "Caen"): 
            self.state = _RETURNING_NEST
        else: 
            self.state = _SEARCHING_PATH

    def next_city(self, pheromones, visiblity): 
        random_number = random.random()
        proba = np.zeros((len(self.to_visit),))
        index_cur = get_key_from_value(dict_cities, self.current_visited_city)
        # add visibility
        # à modifier : ne sommer que sur les villes qui n'ont pas déjà été visité
        somme = 0
        for i in range(len(self.to_visit)): 
            index_next_city = get_key_from_value(dict_cities, self.to_visit[i])
            somme += (pheromones[index_cur, index_next_city ] ** ALPHA) * (visibility[index_cur, index_next_city ] ** BETA)
        for i, city in enumerate(self.to_visit): 
            index_next_city = get_key_from_value(dict_cities, city)
            tau = pheromones[index_cur, index_next_city]
            eta = visibility[index_cur, index_next_city]
            proba[i] = ((tau**(ALPHA) )* (eta**(BETA)))/somme


        # calculate the city to visit 
        if(random_number > 0.5 ):
            next_city = np.argmax(proba)
            next_city = self.to_visit[next_city] 
            next_city = next_city
        else: 
            index = random.randint(0,len(self.to_visit)-1)
            next_city = self.to_visit[index]
        return next_city


    def update_path(self, city): 
        self.visited_cities.append(city)
        self.current_visited_city = city
        # update to visit
        self.to_visit.remove(self.current_visited_city)
            
    def update_path_length(self, city):  
        num_city_current  = get_key_from_value(dict_cities, self.current_visited_city)
        num_city_to_visit = get_key_from_value(dict_cities, city)
        self.path_length += distances[num_city_current, num_city_to_visit]
        return self.path_length
    
    def calculate_path_length(self):  
        inter = combinations(self.visited_cities, 2)

        for tup in inter: 
            id1 = get_key_from_value(dict_cities, tup[0])
            id2 = get_key_from_value(dict_cities, tup[1])
            self.path_length += distances[id1, id2]
        return self.path_length



class goAnt(): 
    def __init__(self, nb_fourmis, villes, pheromones, distances, visibility, evaporation) -> None:
        self.nb_fourmis = nb_fourmis
        self.villes = villes
        self.mat_pheromone = pheromones
        self.mat_distances = distances
        self.mat_pheromones_inter = pheromones*0 
        self.evaporation = evaporation
        self.visibility = visibility 
        # time counter
        self.t =0
        self.NC = 0 #cycle counter
        self.list_ants = {}
        self.all_paths = {}
        self.generate_fourmi()


    def generate_fourmi(self): 
        for i in range(self.nb_fourmis):
            fourmi = Fourmi([dict_cities[i]], self.mat_pheromone, self.visibility) 
            self.list_ants[i] = fourmi 
            self.all_paths[i] = tuple(fourmi.visited_cities )
    
    def run(self, n_simulations): 
        self.len_paths = []
        for j in range(n_simulations):
            for s in range(len(dict_cities)-1) : 
                for i in range(self.nb_fourmis):
                    self.gen_path(i, self.list_ants[i])
                    print("simulation ", j, 'i',"ant ", i, self.list_ants[i].current_visited_city, self.list_ants[i].visited_cities)            
            print([fourmi.path_length for fourmi in self.list_ants.values()])
            len_shortest_path = min([fourmi.path_length for fourmi in self.list_ants.values()])
            self.len_paths.append(len_shortest_path)
        
            self.generate_fourmi()
            self.mat_pheromone = self.mat_pheromones_inter + self.mat_pheromone
            self.mat_pheromones_inter = self.mat_pheromones_inter * 0
        print(self.len_paths)

    def evaporate(self):      # à éxecuter à chaque tour 
        self.mat_pheromone = self.mat_pheromone*0.9
        

    def add_pheromones(self, id1, id2,i): 
        distance_between_cities = distances[id1][id2]
        Q = 2/distance_between_cities
        self.mat_pheromones_inter[id1][ id2] += Q 


    def gen_path(self, i,fourmi): 
        current_city = fourmi.current_visited_city
        next_city = fourmi.next_city(self.mat_pheromone,  visibility)
        fourmi.update_path_length(next_city)
        fourmi.update_path(next_city)
        id1 = get_key_from_value(dict_cities, current_city)
        id2 = get_key_from_value(dict_cities, next_city)
        self.add_pheromones(id1, id2,i)
        self.all_paths[i] += (next_city, )
        return current_city, next_city


    def count_ants_in_city(self, num_city): 
        nb_fourmis_in_city = 0
        for i in range(self.nb_fourmis): 
            if(get_key_from_value(self.list_ants[i].current_visited_city, i) == num_city): 
                nb_fourmis_in_city += 1
        return nb_fourmis_in_city

# ajouter exploration et exploitation


goAntExample = goAnt(nb_fourmis=5, villes=_CITIES, pheromones=pheromones, distances=distances,visibility=visibility, evaporation=EVAPORATION )

goAntExample.run(n_simulations=2)
print(goAntExample.len_paths)

# def goAnt(self):
#     for i in range(len(_CITIES)):
#         n_ants = self.count_ants_in_city(i)
#         for k in range(n_ants): 
#             town_to = self.list_ants[k].next_city()
#             self.evaporate()




# def goAnt():
#     # Retourne le chemin et le cout total trouvé par une fourmi sur son tour
#     # Tous les chemins partent de 0
#     # 0 est bordeaux 
#     chemin = []
#     pos_init = 0
#   # la fourmi se trouve dans la ville de Bordeaux au début 
#     pos = pos_init
#     # choisir le chemin de départ
#     time = 0
#     while(1): #condition la fourmi doit retourner chez elle 
#         # position de la fourmi
#         if(pos == pos_init):
#             break 
        
#         ville_visite = chemin[:,0] #index des villes #chemin = matrix Mx2 C1 = index de la ville C2 = distance parcouru pour arriver à la ville   
        
#         #vérifie si la ville n'est pas déjà visitée    
#         villes_potentiels = [[i,distances[i, pos]]for i in range(len(D)) if i not in villes_visites ]
#         probabilite = np.zeros((2, len(villes_potentiels)))
#         for i in range(len(ville_potentiels)): 
#             index_ville = ville_potentiels[i][0]
#             probabilite[0,i] = (((pheromones[villes_potentiels[i][0],pos])**(alpha)) * ((1/distances[villes_potentiels[i][0],pos])**(beta)))/np.sum((pheromones[villes_potentiels[i][0],pos])**(alpha) * ((1/distances[villes_potentiels[i][0],pos])**(beta)))  
#             probabilite[1,i] = villes_potentiels[i][0]
#         #mettre à jour la matrice des pheromones

#         if(time == 0):
#             probabilite[0,pos] = 0 
        
#         ville_to_visit = np.argmax(probabilite[0,:])
#         index_ville_to_visit = probabilite[1, ville_to_visit]

#         #voir si la ville a déjà été visitée
#         else: 
#             chemin.append([distance[index_ville_to_visit, pos] ,pos])

#         pos = index_ville_to_visit

#     #retourne le chemin
#     return chemin # TODO

# # Ici tout est pret




# for epoch in range(NBEPOCHS):
#     pherobis = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
#     for fourmi in range(NBFOURMIS):
#         chemin, longueur = goAnt()
#         assert longueur > 0
#         deposePhero = Q / longueur 
#         ancienneVille = 0
#         for ville in chemin:
#             pherobis[ancienneVille, ville] += deposePhero
#             ancienneVille = ville

#     pheromones *= EVAPORATION
#     pheromones += pherobis

