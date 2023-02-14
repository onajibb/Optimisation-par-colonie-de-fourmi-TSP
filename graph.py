# ce code a été développé avec le code : https://allophysique.com/posts/python/python_graphes_networkx/

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
from itertools import combinations, permutations

def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35))
,  ("Evry", (48.63, 2.44)))
# , ( "Thiers", (45.85, 3.54)), ("Orléans", (47.90, 47.90)), ("Le Maine", (47.40, -0.60)), (" Le Havre ", (49.494, 0.107)),
#  ("Isere", (45.3633, 5.59)), ("Garonne", (43.604,  1.44305)), ('Loire', (47.168900, -1.469700)),
#  ("Marseille", (43.29648, 5.36978)), ("Saint-denis (La réunion)", (-20.882057, 55.450675)), ("Pointe-à-Pitre (Guadeloupe)", (16.2333, -61.5167)),
#   ("Avignon", ( 43.9493, 4.80559)), ("Beauvais", (49.4294, 2.08064)), ("Basse-terre", (17.302606,  -62.717692)),
#   ("Saint-rose (La réunion)" , (-21.1298300, 55.7962900)),(" Bourgogne ", (47.052505, 4.383721)), (" Cannes ", ( 43.551153,7.011752)))

NBVILLES = len(_CITIES)
print(NBVILLES)
#encodage ville -> nombre 
list_villes = list(np.arange(len(_CITIES)))
noms_villes = [list(_CITIES)[i][0] for i in range(len(_CITIES))]

dict_cities = dict(zip(list_villes, noms_villes))

pos = [_CITIES[i][1] for i in range(len(_CITIES))]
pos = dict(enumerate(pos))

distances = np.zeros(shape=(NBVILLES, NBVILLES), dtype=np.float32)
for i in range(NBVILLES):
    for j in range(NBVILLES):
        distances[i,j] = distance(_CITIES[i][1], _CITIES[j][1])

len_shortest_paths = np.load('len_shortest_path.npy',  allow_pickle='TRUE').item()
shortest_paths = np.load('shortest_paths.npy',  allow_pickle='TRUE').item()
liste = list(len_shortest_paths.values())
arg = np.argmin(np.array(liste))
shortest_path = shortest_paths[arg]
x_axis = np.arange(len(liste))

plt.plot(x_axis, liste)
plt.xlabel("epoch")
plt.ylabel("shortest_path")
plt.grid()
plt.title("Plus court chemin trouvé par epoch")
plt.show()


G = nx.DiGraph()

color= matplotlib.colors.cnames
colormap = dict(enumerate(color.values()))

for i in range(len(dict_cities)): 
    G.add_node(i,label=dict_cities[i],color= colormap[i],pos=pos[i])

colorNodes = [colormap[i] for i in range(len(dict_cities))]
liste = list(G.nodes(data='label'))
labels_nodes = {}
for noeud in liste:
    labels_nodes[noeud[0]]=noeud[1]

for i,j in permutations(dict_cities,2):
    if((i,j) in shortest_path): 
        G.add_edge(i,j,weight=distances[i,j], styl='solid')
    else: 
        G.add_edge(i,j,weight=distances[i,j], styl='thin')

labels_edges = {edge:G.edges[edge]['weight'] for edge in G.edges}
elarge = [(u, v) for (u, v, w) in G.edges(data=True) if w['styl'] == 'solid']
esmall = [(u, v) for (u, v, w) in G.edges(data=True) if w['styl'] == 'thin']

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700,node_color=colorNodes,alpha=0.9)

# labels
nx.draw_networkx_labels(G, pos,
                        font_size=10, 
                         labels=labels_nodes,
                        font_color='black', 
                        font_family='sans-serif')


nx.draw_networkx_edges(G, pos, edgelist=elarge,width=3)
nx.draw_networkx_edges(G, pos, edgelist=esmall,width=1 ,alpha=0.5, edge_color='b')

plt.axis('off')
plt.title("Graphe représentant et le plus court chemin hamiltonien")
plt.show()