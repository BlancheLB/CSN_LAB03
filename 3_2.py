"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""

import networkx as nx
from networkx.algorithms.centrality import closeness
import numpy as np


# load in the files and make adjacency lists
languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
adjacency_matrices = {}
sequences_matrices=[]
nodes=[]

def read_files():
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
                nodes.append(words)
                if  words[0]!=words[1]:
                    if words[0] in adjacency_matrix.keys():
                        adjacency_matrix[words[0]].append(words[1])
                    else:
                        adjacency_matrix[words[0]] = [words[1]] 
        sequences_matrices.append([lang,nodes])   
    #print(adjacency_matrices["English"])
         

 

def closeness_normal_graph(dict):
    closeness_adjacency_matrices ={}
    tab=[]
    for lang in languages:
        G = nx.Graph(dict[lang]) 
        closeness_adjacency_matrices[lang]= nx.algorithms.centrality.closeness_centrality(G)
    print(closeness_adjacency_matrices)
    return closeness_adjacency_matrices,tab


read_files()
closeness_SM=[]
#print(adjacency_matrices["English"])
dict,arr=closeness_normal_graph(adjacency_matrices)
np.savetxt('closeness_arr.csv', arr, delimiter=',')
np.savetxt('closeness_dict.csv', dict, delimiter=',')









