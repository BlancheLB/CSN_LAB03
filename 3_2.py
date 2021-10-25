"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""

import networkx as nx
from networkx.algorithms.centrality import closeness
import numpy as np
import random




"""
load the edges per language from the files
"""
def read_files(languages):
    adjacency_matrices = {}
    sequences_matrices=[]
    for lang in languages:
        graph_file = open('dependency_networks/' + lang + "_syntactic_dependency_network.txt",encoding='UTF8')
        count = 0
        adjacency_matrices[lang] = {}
        adjacency_matrix = adjacency_matrices[lang]
        while True:
            count += 1
            line = graph_file.readline()
            if not line:
                print("Loaded " + str(count-1) + " lines from language " + lang)
                break
            else:
                line = line.strip() # remove
                words = line.split(' ') # split on space
                if len(words) > 2:
                    print("warning: weird line - more than 2 words", line)
                if len(words) < 2:
                    print("warning: weird line - less than 2 words", line)
                    continue
                # nodes.append(words)
                if  words[0]!=words[1]:
                    if words[0] in adjacency_matrix.keys():
                        adjacency_matrix[words[0]].append(words[1])
                    else:
                        adjacency_matrix[words[0]] = [words[1]] 
        # TODO: i removed this because i dont see the use
        # sequences_matrices.append([lang,nodes])   
    #print(adjacency_matrices["English"])
    return adjacency_matrices, sequences_matrices
         
     

def closeness_normal_graph(dict):
    closeness_adjacency_matrices ={}
    tab=[]
    for lang in languages:
        G = nx.Graph(dict[lang]) 
        closeness_adjacency_matrices[lang]= nx.algorithms.centrality.closeness_centrality(G)
    print(closeness_adjacency_matrices)
    return closeness_adjacency_matrices,tab


"""
Get the closeness centraility of a node
If it has a neighbor that only has one edge, also returns the closeness
centrality of that node
"""
def node_closeness_centrality(graph, node):
    lengths = nx.algorithms.shortest_paths.generic.shortest_path_length(graph, source=node)
    closeness_centralities = {node: (len(graph.nodes) - 1)/ (sum(lengths.values()))}
    # if node has neighbours that only have one edge, return their cs also
    for n in graph.neighbors(node):
        # if only one edge, calculate at the end
        if len(list(graph.neighbors(n))) == 1:
            lengths_plus_1 = [l + 1 for l in lengths.values()]
            closeness_centralities[n] = (len(graph.nodes) - 1)/ (sum(lengths_plus_1))
    return closeness_centralities
    # return nx.algorithms.centrality.closeness_centrality(graph, node)



languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
languages_to_use = languages[1:2]
# load files
adjacency_matrices, sequence_matrices = read_files(languages_to_use)
# print(adjacency_matrices)
# load into graphs
graphs = {}
for lang in languages_to_use:
    graphs[lang] = nx.Graph(adjacency_matrices[lang])

# get the closeness centralities per node
"""
closeness_centralities = {l: {} for l in languages_to_use}
for lang in languages_to_use:
    c_s_lang = closeness_centralities[lang]
    for n in graphs[lang].nodes:
        if n not in c_s_lang.keys():
            c_s_lang = c_s_lang | node_closeness_centrality(graphs[lang], n)
print(closeness_centralities)
"""

# different orderings:
print()
by_degree_desc = [n for (n,_) in sorted(graphs['Basque'].degree, key=lambda x: x[1], reverse=True)]
by_degree_asc = [n for (n,_) in sorted(graphs['Basque'].degree, key=lambda x: x[1], reverse=False)]
random_order = graphs['Basque'].nodes.copy()
random.shuffle(random_order)

closeness_SM=[]
# dict,arr=closeness_normal_graph(adjacency_matrices)
# np.savetxt('closeness_arr.csv', arr, delimiter=',')
# np.savetxt('closeness_dict.csv', dict, delimiter=',')









