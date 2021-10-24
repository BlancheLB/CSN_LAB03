"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""
import random
import math
import networkx as nx
from networkx.algorithms.centrality import closeness

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
                if words[0] in adjacency_matrix.keys():
                    adjacency_matrix[words[0]].append(words[1])
                else:
                    adjacency_matrix[words[0]] = [words[1]] 
        sequences_matrices.append([lang,nodes])   
    print(adjacency_matrices["English"])
         



def switching_model(mat,Q,E):
    n=int(Q*E);
    for i in range(n):
        #index of two random nodes to exchange edge
        index1=random.randint(1,len(mat)-1)
        index2=random.randint(1,len(mat)-1)
        
        mat[index1][1],mat[index2][1]=mat[index2][1],mat[index1][1]
    return mat
        
def switchM_all(mat_languages,closseness):
    for i in range(len(mat_languages)):
        E=int(mat_languages[i][1][0][1])
        Q=math.log(E)
        switching_model(mat_languages[i][1],Q,E)
        closeness(mat_languages[i],closseness)
    
    return mat_languages,closseness


def closseness(degree_sequence,closseness):
     # calculate closeness centrality per edge
    closeness_centrality_i = nx.algorithms.centrality.closeness_centrality(degree_sequence)
    #print(closeness_centrality_i)
    N = len(closeness_centrality_i)
    closeness_centrality = 0
    # calculate closeness centrality of the entire graph
    for i in closeness_centrality_i.values():
        closeness_centrality += i/N
        closseness.append(closeness_centrality)
    return closseness

read_files()
closeness_SM=[]
print(adjacency_matrices["English"])
switchM_all(sequences_matrices,closeness_SM)


#switching_model(sequences_matrices[5][1],1,1)








