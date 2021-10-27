"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""

import networkx as nx
from networkx.algorithms.centrality import closeness
import numpy as np
import random
import math
from networkx.utils import py_random_state



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
                # avoid loops
                if  words[0]!=words[1]:
                    if words[0] in adjacency_matrix.keys():
                        adjacency_matrix[words[0]].append(words[1])
                    else:
                        adjacency_matrix[words[0]] = [words[1]] 
        # sequences_matrices.append([lang,nodes])   
    #print(adjacency_matrices["English"])
    return adjacency_matrices, sequences_matrices
         


"""
Calculate the closeness centraility of a node
If it has a neighbor that only has one edge, also returns the closeness
centrality of that node
"""
def node_closeness_centrality(graph, node):
    lengths = nx.algorithms.shortest_paths.generic.shortest_path_length(graph, source=node)
    dist_sum = sum(lengths.values())
    # if not connected return 0
    if dist_sum == 0:
        return {node: 0}
    closeness_centralities = {node: (len(lengths))/ dist_sum}
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
Giving a smaller than value means the calculation stops as soons as it is sure the value is less than the given value
With milestones set to true, it returns the progress of c_s over percnetage
"""
def graph_closeness_centrality(graph, node_order=None, fraction=1, smaller_than_value=None, milestones = False):

    # change order of nodes if requested
    nodes = None
    if node_order is None:
        nodes = list(graph.nodes)
    elif node_order == "random":
        nodes = list(graph.nodes).copy()
        random.shuffle(nodes)
    elif node_order == "degree_desc":
        nodes = [n for (n,_) in sorted(graph.degree, key=lambda x: x[1], reverse=True)]
    elif node_order == "degree_asc":
        nodes = [n for (n,_) in sorted(graph.degree, key=lambda x: x[1], reverse=False)]
    else:
        print("unknown noder_order, defaulting to normal order")
        node_order = list(graph.nodes)
    print("👏 done ordering")
    # calculate for only a fraction of the nodes
    if fraction < 1:
        assert fraction > 0
        nodes = nodes[0:int(len(nodes)*fraction)]

    # calculate node closeness centrality for all selected nodes
    c_s_graph = {}
    N = graph.number_of_nodes()

    milestone_nr = 1
    milestone_step = N/200
    milestone_hist = {}

    for n in nodes:
        if n not in c_s_graph.keys(): # because it might have already been calculated
            c_s_node = node_closeness_centrality(graph, n)
            c_s_graph = c_s_graph | c_s_node
            count = len(c_s_graph)
            # if it is already clear it wont be higher than the 'smaller_than_value', return
            # in accordance with formula (6) in the asignment
            if smaller_than_value != None and count % 1000 == 0:
                if  smaller_than_value > (sum(c_s_graph.values())/N + 1 - count/N):
                    print("Sure it is less than the value after ", count, "/", N, " words")
                    break
            if milestones == True:
                if count > milestone_nr*milestone_step:
                    milestone_hist[milestone_nr] = sum(c_s_graph.values())/len(c_s_graph)
                    milestone_nr += 1
    if not milestones:
        # calculate graph closeness centrality
        return sum(c_s_graph.values())/len(c_s_graph)
    else:
        milestone_hist[milestone_nr] = sum(c_s_graph.values())/len(c_s_graph)
        return milestone_hist

"""
returns a erdos-renyi graph with the given number of nodes and edges
"""
def create_erdos_graph(nr_of_nodes: int, nr_of_edges: int):
    n = nr_of_nodes
    m = nr_of_edges
    # probablity of edge
    p = m/n
    
    # generate erdos-renyi graph
    g = nx.gnm_random_graph(n,m)
    # g = nx.generators.random_graphs.erdos_renyi_graph(n, p, directed=False)
    return g

"""
apply the switching model to the graph
"""
def apply_switching_model(graph, Q:int=None):
    #calculate Q according to coupon collector's problem
    if Q == None:
        Q = math.log(graph.number_of_edges())
    number_of_tries = int(graph.number_of_edges() * Q)
    # switch edges randomly
    double_edge_swap(graph,nswap=number_of_tries)
    return graph


"""
Perform edge swaps
Modified version of https://networkx.org/documentation/stable/_modules/networkx/algorithms/swap.html
"""
@py_random_state(2)
def double_edge_swap(G, nswap=1, seed=None):
    if G.is_directed():
        raise nx.NetworkXError("double_edge_swap() not defined for directed graphs.")
    if len(G) < 4:
        raise nx.NetworkXError("Graph has less than four nodes.")
    # Instead of choosing uniformly at random from a generated edge list,
    # this algorithm chooses nonuniformly from the set of nodes with
    # probability weighted by degree.
    n = 0
    swapcount = 0
    keys, degrees = zip(*G.degree())  # keys, degree
    cdf = nx.utils.cumulative_distribution(degrees)  # cdf of degree
    discrete_sequence = nx.utils.discrete_sequence
    while swapcount < nswap:
        #        if random.random() < 0.5: continue # trick to avoid periodicities?
        # pick two random edges without creating edge list
        # choose source node indices from discrete distribution
        (ui, xi) = discrete_sequence(2, cdistribution=cdf, seed=seed)
        if ui == xi:
            swapcount += 1
            continue  # same source, skip
        u = keys[ui]  # convert index to label
        x = keys[xi]
        # choose target uniformly from neighbors
        v = seed.choice(list(G[u]))
        y = seed.choice(list(G[x]))
        if v == y:
            swapcount += 1
            continue  # same target, skip
        if (x not in G[u]) and (y not in G[v]):  # don't create parallel edges
            G.add_edge(u, x)
            G.add_edge(v, y)
            G.remove_edge(u, v)
            G.remove_edge(x, y)
            swapcount += 1
        n += 1
    return G