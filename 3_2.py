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
Calculate the closeness centraility of a node
If it has a neighbor that only has one edge, also returns the closeness
centrality of that node
"""
def node_closeness_centrality(graph, node):
    lengths = nx.algorithms.shortest_paths.generic.shortest_path_length(graph, source=node)
    closeness_centralities = {node: (len(lengths))/ (sum(lengths.values()))}
    if closeness_centralities[node] > 100:
        print("high value detected:", closeness_centralities[node], lengths)
    # if node has neighbours that only have one edge, return their cs also
    for n in graph.neighbors(node):
        if len(list(graph.neighbors(n))) == 1:
            lengths_plus_1 = [l + 1 for l in lengths.values()]
            closeness_centralities[n] = (len(lengths) - 1)/ (sum(lengths_plus_1))
    return closeness_centralities
    # return nx.algorithms.centrality.closeness_centrality(graph, node)

"""
Calculate the closeness centrality of the full graph
Presenting a graph order is optional
Giving what percentage of the nodes should be used for the calculation is optional
"""
def graph_closeness_centrality(graph, node_order=None, fraction=1):

    # change order of nodes if requested
    nodes = None
    if node_order is None:
        nodes = graph.nodes
    elif node_order == "random":
        nodes = graph.nodes.copy()
        random.shuffle(nodes)
    elif node_order == "degree_desc":
        nodes = [n for (n,_) in sorted(graphs['Basque'].degree, key=lambda x: x[1], reverse=True)]
    elif node_order == "degree_asc":
        nodes = [n for (n,_) in sorted(graphs['Basque'].degree, key=lambda x: x[1], reverse=False)]
    else:
        print("unknown noder_order, defaulting to normal order")
        node_order = graph.nodes
    
    # calculate for only a fraction of the nodes
    if fraction < 1:
        assert fraction > 0
        nodes = list(nodes)[0:int(len(nodes)*fraction)]

    # calculate node closeness centrality for all selected nodes
    c_s_graph = {}
    for n in nodes:
        if n not in c_s_graph.keys(): # because it might have already been calculated
            c_s_graph = c_s_graph | node_closeness_centrality(graph, n)
    # calculate graph closeness centrality
    return sum(c_s_graph.values())/len(c_s_graph)


def main():
    languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
    languages_to_use = languages[1:2]
    # load files
    adjacency_matrices, sequence_matrices = read_files(languages_to_use)

    # load into graphs
    graphs = {}
    for lang in languages_to_use:
        graphs[lang] = nx.Graph(adjacency_matrices[lang])

    # get the closeness centralities per node
    closeness_centralities = {l: {} for l in languages_to_use}
    for lang in languages_to_use:
        c_s_lang = graph_closeness_centrality(graphs[lang], node_order=None, fraction=0.1)
    print(c_s_lang)


    # closeness_SM=[]
    # dict,arr=closeness_normal_graph(adjacency_matrices)
    # np.savetxt('closeness_arr.csv', arr, delimiter=',')
    # np.savetxt('closeness_dict.csv', dict, delimiter=',')



if __name__ == "__main__":
    main()


