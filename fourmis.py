import numpy as np
from itertools import combinations, permutations
import time
import random
import matplotlib
import pickle 

# https://github.com/Akavall/AntColonyOptimization/blob/master/ant_colony.py

# les positions des villes sont fictifs et calculée par Oliver Problem 30 https://stevedower.id.au/research/oliver-30

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)))

#("Evry", (48.63, 2.44)), 
# ( "Thiers", (45.85, 3.54)), ("Orléans", (47.90, 47.90)), ("Le Maine", (47.40, -0.60)), (" Le Havre ", (49.494, 0.107)),
#  ("Isere", (45.3633, 5.59)), ("Garonne", (43.604,  1.44305)), ('Loire', (47.168900, -1.469700)),
#  ("Marseille", (43.29648, 5.36978)), ("Saint-denis (La réunion)", (-20.882057, 55.450675)), ("Pointe-à-Pitre (Guadeloupe)", (16.2333, -61.5167)),
#   ("Avignon", ( 43.9493, 4.80559)), ("Beauvais", (49.4294, 2.08064)), ("Basse-terre", (17.302606,  -62.717692)),
#   ("Saint-rose (La réunion)" , (-21.1298300, 55.7962900)),(" Bourgogne ", (47.052505, 4.383721)), (" Cannes ", ( 43.551153,7.011752)))



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

NBFOURMIS = 10
NBEPOCHS = 500
NBVILLES = len(_CITIES)
ALPHA = 5
BETA = 5
EVAPORATION = 0.5
COEFFEXPLORATION = 0.1
Q = 1000
C = 0.2
distances = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
pheromones = C + np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
visibility = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
# définir la ville de départ 

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
        self.s = len(self.visited_cities)
        inter = self.visited_cities
        self.to_visit=[]
        random_number = random.random()
        for ville in noms_villes:
            self.to_visit.append(ville)
        # la ville visité par la fourmi
        self.current_visited_city = self.visited_cities[-1]
        # la ville à visiter par la fourmi
        self.current_city_to_visit = None
        # la distance totale parcouru 
        self.path_length = 0
        self.path_length = self.calculate_path_length()
        # état de la fourmi

        self.edges = []
        self.time = 0 
        self.mat_pheromones = pheromones


    def next_city(self, mat_pheromones, visiblity): 
        random_number = random.random()
        proba = np.zeros((len(dict_cities),))
        index_cur = get_key_from_value(dict_cities, self.current_visited_city)
        # add visibility
        # à vérifier : ne sommer que sur les villes qui n'ont pas déjà été visité
        somme = 0
        for i in range(len(self.to_visit)): 
            index_next_city = get_key_from_value(dict_cities, self.to_visit[i])
            
            somme += (mat_pheromones[index_cur, index_next_city ] ** ALPHA) * (visibility[index_cur, index_next_city ] ** BETA)
            
        for city in self.to_visit: 
            index_next_city = get_key_from_value(dict_cities, city)

            tau = mat_pheromones[index_cur, index_next_city]
            eta = visibility[index_cur, index_next_city]

            proba[index_next_city] = ((tau**(ALPHA) )* (eta**(BETA)))/somme

        # calculate the city to visit 
        if(random_number > COEFFEXPLORATION ):
            next_city = np.argmax(proba)
            next_city = dict_cities[next_city]

        else: 
            index = random.randint(0,len(self.to_visit)-1)
            next_city = self.to_visit[index]
        return next_city


    def update_path(self, city): 
        self.current_visited_city = city
        self.to_visit.remove(self.current_visited_city)
        self.s += 1
        
            
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
    def __init__(self, nb_fourmis, villes, pheromones,  visibility, evaporation) -> None:
        self.nb_fourmis = nb_fourmis
        self.villes = villes
        self.mat_pheromone = pheromones
        self.mat_distances = distances
        self.mat_pheromones_inter = pheromones*0 
        self.evaporation = evaporation
        self.visibility = visibility 
        self.list_ants = {}
        self.all_paths = {}
        self.len_shortest_paths = {}
        # time counter
        self.t =0
        self.NC = 0 #cycle counter
        self.shortest_paths= {}
        self.generate_fourmi()
        


    def generate_fourmi(self): 
        for i in range(self.nb_fourmis):
            a = random.randint(0,len(dict_cities)-1)
            fourmi = Fourmi([dict_cities[a]], self.mat_pheromone, self.visibility) 
            self.list_ants[i] = fourmi 
            self.all_paths[i] = tuple(fourmi.visited_cities )
    
    def run(self, n_simulations): 
        
        for j in range(n_simulations):
            for s in range(len(dict_cities)) : 
                for i in range(self.nb_fourmis):
                    (id1, id2) = self.gen_path(i, self.list_ants[i])


                    self.list_ants[i].edges.append((id1, id2))
                
            for f in range(self.nb_fourmis):  
                self.list_ants[f].to_visit.append(self.list_ants[f].visited_cities[0])

                id1, id2 = get_key_from_value(dict_cities, self.list_ants[f].current_visited_city), get_key_from_value(dict_cities,self.list_ants[f].visited_cities[0])
                self.list_ants[f].update_path_length(self.list_ants[f].visited_cities[0] )
                self.list_ants[f].update_path(self.list_ants[f].visited_cities[0] )
                self.list_ants[i].edges.append((id1, id2))
            len_shortest_path = min([fourmi.path_length for fourmi in self.list_ants.values()])
            print("simulation ", j, "shortest path", len_shortest_path)  
            argmin = np.argmin(np.array([fourmi.path_length for fourmi in self.list_ants.values()]))
            self.shortest_paths[j] = self.list_ants[argmin].edges
            self.len_shortest_paths[j]=len_shortest_path
            for (i,j) in permutations(dict_cities,2):
                for f in range(self.nb_fourmis):  
                    Lk = self.list_ants[f].path_length
                    if (i,j) in self.list_ants[f].edges: 
                        self.add_pheromones(i,j, Lk)
            # time.sleep(5)
            self.update_tour()
            
            

    def update_tour(self):      # à éxecuter à chaque tour 
        self.mat_pheromone = self.mat_pheromone*0.9 + self.mat_pheromones_inter
        self.NC+=1
        self.t +=1
        self.mat_pheromones_inter = self.mat_pheromones_inter * 0
        for i in range(self.nb_fourmis): 
            self.list_ants[i].__init__([self.list_ants[i].current_visited_city], self.mat_pheromone, self.visibility)
        self.generate_fourmi()
        

    def add_pheromones(self, id1, id2,Lk): 
        to_add = Q/Lk
        self.mat_pheromones_inter[id1][ id2] += to_add 


    def gen_path(self, i,fourmi): 
        current_city = fourmi.current_visited_city
        next_city = fourmi.next_city(self.mat_pheromone,  visibility)
        fourmi.update_path_length(next_city)
        fourmi.update_path(next_city)
        id1 = get_key_from_value(dict_cities, current_city)
        id2 = get_key_from_value(dict_cities, next_city)
        #self.add_pheromones(id1, id2)
        self.all_paths[i] += (next_city, )
        return id1, id2





goAntExample = goAnt(nb_fourmis=10, villes=_CITIES, pheromones=pheromones,visibility=visibility, evaporation=EVAPORATION )

goAntExample.run(n_simulations=50)

np.save('len_shortest_path.npy', goAntExample.len_shortest_paths)
np.save('shortest_paths.npy', goAntExample.shortest_paths)
