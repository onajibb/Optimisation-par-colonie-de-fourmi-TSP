# https://allophysique.com/posts/python/python_graphes_networkx/

import networkx as nx
import matplotlib.pyplot as plt 
from fourmis import *

print(goAntExample.len_shortest_paths)
shortest_path = goAntExample.shortest_paths[argmin]

print("shortest path :", shortest_path)
G = nx.DiGraph()

pos = {0 :(44.833333,-0.566667), 1: (48.8566969,2.3514616), 2: (43.7009358,7.2683912),
3: (45.7578137,4.8320114),4: (47.2186371,-1.5541362), 5 : (48.4,-4.483333),6: (50.633333,3.066667),
7: (45.783333,3.083333),8: (48.583333,7.75), 9: (46.583333,0.333333) ,
10: (47.466667,-0.55),11: (43.6,3.883333),12: (49.183333,-0.35)}

color= matplotlib.colors.cnames
colormap = dict(enumerate(color.values()))

for i in range(len(dict_cities)): 
    G.add_node(i,label=dict_cities[i],color= colormap[i],pos=pos[i])

print(G.nodes)
colorNodes = [colormap[i] for i in range(len(dict_cities))]


for i,j in permutations(dict_cities,2):
    if((i,j) in shortest_path): 
        print(i,j)
        G.add_edge(i,j,weight=distances[i,j], styl='solid')
    else: 
        G.add_edge(i,j,weight=distances[i,j], styl='thin')
        
labels_edges = {edge:G.edges[edge]['weight'] for edge in G.edges}

elarge = [(u, v) for (u, v, w) in G.edges(data=True) if w['styl'] == 'solid']
print(elarge)
esmall = [(u, v) for (u, v, w) in G.edges(data=True) if w['styl'] == 'thin']
# nodes
nx.draw_networkx_nodes(G, pos, node_size=700,node_color=colorNodes,alpha=0.9)

# labels
nx.draw_networkx_labels(G, pos,
                        font_size=10, 
                        font_color='black', 
                        font_family='sans-serif')

# edges
 # edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,width=3)
nx.draw_networkx_edges(G, pos, edgelist=esmall,width=1 ,alpha=0.5, edge_color='b')
    


plt.axis('off')
# nx.draw_networkx_edge_labels(G, pos,edge_labels=labels_edges, font_color='red')


plt.show()