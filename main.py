from helper_functions import *
import json
import concurrent.futures

"""
calculates the closeness centrality for all the languages and outputes to file
"""
def calc_lang_c_s():
    languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
    languages_to_use = languages
    # load files
    adjacency_matrices, sequence_matrices = read_files(languages_to_use)

    # load into graphs
    graphs = {}
    for lang in languages_to_use:
        graphs[lang] = nx.Graph(adjacency_matrices[lang])
    print("📈 loaded all files into graphs")
    # get the closeness centralities per language graph
    closeness_centralities = {l: {} for l in languages_to_use}
    # calculate in multiple threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_lang = {executor.submit(graph_closeness_centrality, graphs[lang], node_order=None, fraction=1): lang for lang in languages_to_use}
        print("submitted all tasks to queue")
        for future in concurrent.futures.as_completed(future_to_lang):
            lang = future_to_lang[future]
            try:
                closeness_centralities[lang] = future.result()
                print("✅ closeness centrality for ", lang, " calculated")
            except:
                print("❌ failed to calculate for ", lang)
    with open('output/language_c_s.json', 'w') as f:
        f.write(json.dumps(closeness_centralities))
    print("💯 all done")


def calculate_p_value(original_graph, c_s_original):
    erdos = create_erdos_graph(nr_of_nodes=original_graph.number_of_nodes(), nr_of_edges=original_graph.number_of_edges())

"""
Test how correct the closeness centrality is after calculating for percentage of the nodes
"""
def c_t_after_percentage(ordering):
    languages = ['English']
    languages_to_use = languages
    # load files
    adjacency_matrices, sequence_matrices = read_files(languages_to_use)

    # load into graphs
    graph= nx.Graph(adjacency_matrices['English'])
    print("📈 loaded file into graph")

    closeness_centralities = graph_closeness_centrality(graph, node_order=ordering, fraction=1, milestones=True)

    if ordering == None:
        ordering = 'normal'
    with open('output/percentages_c_s' + ordering + '.json', 'w') as f:
        f.write(json.dumps(closeness_centralities))
    print("💯 all done")




def main():
    # calc_lang_c_s()

    for ordering in ['random', 'degree_asc', 'degree_desc', None]:
        c_t_after_percentage(ordering)

    # closeness_SM=[]
    # dict,arr=closeness_normal_graph(adjacency_matrices)
    # np.savetxt('closeness_arr.csv', arr, delimiter=',')
    # np.savetxt('closeness_dict.csv', dict, delimiter=',')



if __name__ == "__main__":
    main()

