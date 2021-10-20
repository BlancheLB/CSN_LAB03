"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""
import random
import math

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
         
    #print(adjacency_matrices["English"])


def switching_model(mat,Q,E):
    n=int(Q*E);
    for i in range(n):
        #index of two random nodes to exchange edge
        index1=random.randint(1,len(mat)-1)
        index2=random.randint(1,len(mat)-1)
        
        mat[index1][1],mat[index2][1]=mat[index2][1],mat[index1][1]
    return mat
        
def switchM_all(mat_languages):
    for i in range(len(mat_languages)):
        E=int(mat_languages[i][1][0][1])
        Q=math.log(E)
        switching_model(mat_languages[i][1],Q,E)
    return mat_languages

read_files()
switchM_all(sequences_matrices)

#switching_model(sequences_matrices[5][1],1,1)








