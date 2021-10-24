import random
import math
import pandas as pd
import numpy as np
import networkx as nx
from networkx import *


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
                if  words[0]!=words[1] and count!=1:
                    if words[0] in adjacency_matrix.keys():
                        adjacency_matrix[words[0]].append(words[1])
                    else:
                        adjacency_matrix[words[0]] = [words[1]] 
        sequences_matrices.append([lang,nodes])   
    #print(adjacency_matrices["English"])
         







read_files()
closeness_SM=[]
#print(adjacency_matrices["English"].items())
a=list(adjacency_matrices)
print(a[5])


g=adjacency_matrices["English"]

G=nx.Graph(g)
E=G.number_of_edges()
print(E)
Q=math.log(E)
n=int((Q*E))
print(list(G.edges_iter(0)))
for n in G.nodes():
    print(nx.algorithms.centrality.harmonic_centrality(G,G[n]))
Z=nx.double_edge_swap(G,n,max_tries=100*n)
print(G)
print(Z)



