import networkx as nx

# number of vertices
n = 1000
# number of wanted edges
m = 100
# probablity of edge
p = m/n


results = []

for i in range(0,10):
    # generate erdos-renyi graph
    g = nx.generators.random_graphs.erdos_renyi_graph(n, p, directed=True)
    
    # calculate closeness centrality per edge
    closeness_centrality_i = nx.algorithms.centrality.closeness_centrality(g)
    #print(closeness_centrality_i)
    N = len(closeness_centrality_i)
    closeness_centrality = 0
    # calculate closeness centrality of the entire graph
    for i in closeness_centrality_i.values():
        closeness_centrality += i/N
    
    results.append(closeness_centrality)
print(results)
