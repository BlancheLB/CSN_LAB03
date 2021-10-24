"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""
import random
import math
import networkx as nx
from networkx.algorithms.centrality import closeness
import numpy as np
import math
import pandas as pd

from test import switching_model



languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
adjacency_matrices = {}

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
                if  words[0]!=words[1] and count!=1:
                    if words[0] in adjacency_matrix.keys():
                        adjacency_matrix[words[0]].append(words[1])
                    else:
                        adjacency_matrix[words[0]] = [words[1]] 
    #print(adjacency_matrices["English"])
    return adjacency_matrices



def sample_graph(G):
    #take randomly 10% of the graph G
    return G

def Cmin(G,Cprevious,nodei):        
    if Cprevious==0:
        C=nx.algorithms.centrality.closeness_centrality(G,G[nodei])
        #C=nx.algorithms.centrality.harmonic_centrality(G,G[nodei])
        return C
    return (nx.algorithms.centrality.closeness_centrality(G,G[nodei])+Cprevious)/G.number_of_nodes()
    #return (nx.algorithms.centrality.harmonic_centrality(G,G[nodei])+Cprevious)/G.number_of_nodes()

def Cmax(Cmin,M,N):
    return Cmin+1-M/N

def null_hypothesis(Clang,G):
    M=cmin=cmax=0
    N=G.number_of_nodes()
    for n in G.nodes():
        cmin=Cmin(G,n)
        cmax=Cmax(cmin,M,N)
        if Clang < cmin:
            return 1
        if cmax < Clang:
            return 0
        else: M+=1
    return 0



def monteCarlo(G,C,x):
    nsuccess_Bin=nsuccess_switch_model=nsuccess_sample=0
    num_nodes=G.number_of_nodes()
    num_edges=G.number_of_edges()
    Cprevious_Bin=Cprevious_SM=Cprevious_Sample=0

    Q=math.log(num_edges)
    x=round(Q*num_edges)
    for i in range (x):

        #generate random graph erdos Reyni
        gBin = nx.generators.random_graphs.gnm_random_graph(num_nodes,num_edges, directed=True)

        #generate random grapgh with switching model
        gSM =nx.double_edge_swap(G,x,max_tries=100*x)

        #generate sample : 10% of G
        g10 =sample_graph(G)

        #Closeness centrality :

        #Erdos Reyni
        nsuccess_Bin+=null_hypothesis(C,gBin)
        
        #Switching Model
        nsuccess_switch_model+=null_hypothesis(C,gSM)
        
        #Switching Model
        nsuccess_sample+=0#null_hypothesis(C,g10)

        

    return nsuccess_Bin,nsuccess_switch_model,nsuccess_sample


def main():
    n=10 # number of monte carlo repetition
    adjacency_matrices=read_files()
   
    G=nx.Graph(adjacency_matrices["English"])
    C=nx.algorithms.centrality.closeness_centrality(G)
    #C=nx.algorithms.centrality.harmonic_centrality(G)

    nsuccess_Bin,nsuccess_switch_model,nsuccess_sample=monteCarlo(G,C,n)

    p_value_Bin=nsuccess_Bin/n
    p_value_SM=nsuccess_switch_model/n
    p_value_sample=nsuccess_sample/n


    



   


if __name__ == "__main__":
    main()


