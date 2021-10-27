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
    languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
    languages_to_use = languages
    # load files
    adjacency_matrices, sequence_matrices = read_files(languages_to_use)

    # load into graphs
    graphs= {l: nx.Graph(adjacency_matrices[l]) for l in languages_to_use}
    print("📈 loaded file into graph")

    closeness_centralities = {lang: {} for lang in languages_to_use}
    for l in languages:
        closeness_centralities[l] = graph_closeness_centrality(graphs[l], node_order=ordering, fraction=0.05, milestones=True)
        print("done with", l)

    if ordering == None:
        ordering = 'normal'
    with open('output/percentages_c_s' + ordering + '.json', 'w') as f:
        f.write(json.dumps(closeness_centralities))
    print("💯 all done")


def p_tests():
    languages = ['Basque', 'Greek',  'Turkish']

    #languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
    languages_to_use = languages
    # load files
    adjacency_matrices, sequence_matrices = read_files(languages_to_use)

    # load into graphs
    graphs = {}
    for lang in languages_to_use:
        graphs[lang] = nx.Graph(adjacency_matrices[lang])
    print("📈 loaded all files into graphs")

    # get the closeness centralities per language from file
    with open('output/language_c_s_full.json','r') as f:
        closeness_centralities = json.load(f)

    T = 20
    fraction = 0.05
    measurements_erdos = {l: {}  for l in languages_to_use}
    measurements_switching =  {l: {}  for l in languages_to_use}

    for lang in languages_to_use:
        nr_of_nodes = graphs[lang].number_of_nodes()
        nr_of_edges = graphs[lang].number_of_edges()
        # first run erdos-renyi
        iters = [i for i in range(0,T)]
        for i in iters:
            erdos_renyi_graph = create_erdos_graph(nr_of_nodes, nr_of_edges)
            measurements_erdos[lang][i] = graph_closeness_centrality(erdos_renyi_graph, node_order=None, fraction=fraction)
            with open('output/ptest_' +'erdos' +'.json', 'w') as f:
                f.write(json.dumps(measurements_erdos))
            print("renyi", lang, i, "/", T, "done")
        print("✅ done with erdos graphs of", lang)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            
        #     erdos_renyi_graphs = [create_erdos_graph(nr_of_nodes, nr_of_edges) for i in iters]
        #     print("created all erdos-renyi graphs")
        #     future_to_iter = {executor.submit(graph_closeness_centrality, erdos_renyi_graphs[i], node_order=None, fraction=fraction): i for i in iters}
        #     print("submitted all tasks to queue")
        #     for future in concurrent.futures.as_completed(future_to_iter):
        #         iter = future_to_iter[future]
        #         try:
        #             closeness_centralities[iter] = future.result()
        #             print("✅ closeness centrality erdos-renyi nr", iter ,"calculated")
        #         except:
        #             print("❌ failed to calculate nr", iter)
        

    
    # for switching model
    for lang in languages:
        nr_of_nodes = graphs[lang].number_of_nodes()
        nr_of_edges = graphs[lang].number_of_edges()
        # first run erdos-renyi
        iters = [i for i in range(0,T)]
        for i in iters:
            switching_graph = graphs[lang].copy()
            apply_switching_model(switching_graph)
            measurements_switching[lang][i] = graph_closeness_centrality(switching_graph, node_order=None, fraction=fraction)
            with open('output/ptest_' +'switched' +'.json', 'w') as f:
                f.write(json.dumps(measurements_switching))
            print("switching", lang, i, "/", T, "done")
        print("✅ done with switching graphs of", lang)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #     iters = [i for i in range(0,T)]
        #     switched_graphs = []
        #     for i in iters:
        #         g = graphs[lang].copy()
        #         apply_switching_model(g)
        #         switched_graphs.append(g)
        #     print("created all swtiching model graphs")
        #     future_to_iter = {executor.submit(graph_closeness_centrality, switched_graphs[i], node_order=None, fraction=fraction): i for i in iters}
        #     print("submitted all tasks to queue")
        #     for future in concurrent.futures.as_completed(future_to_iter):
        #         iter = future_to_iter[future]
        #         try:
        #             closeness_centralities[iter] = future.result()
        #             print("✅ closeness centrality switched nr", iter ,"calculated")
        #         except:
        #             print("❌ failed to calculate nr", iter)
        
    print("💯 all done")

def p_value():
    #upload closeness centrality
    with open('./output/ptest_erdos.json','r') as f:
        dataErdos = json.load(f)
    with open('./output/ptest_switched.json','r') as f:
        dataSwitched = json.load(f)
    with open('./output/language_c_s_full.json','r') as f:
        dataC= json.load(f)
    
    #calculate p_value of erdos graphs
    p_value_erdos =  {l: {}  for l in dataErdos.keys()}
    for lang in dataErdos.keys():
        num_success=0
        for i in range(len(dataErdos[lang].values())):
            if(dataC[lang]>= dataErdos[lang][str(i)]):
                num_success+=1
        p_value_erdos[lang]=(num_success/len(dataErdos[lang].values()))
    with open('output/p_value_erdos.json', 'w') as f:
        f.write(json.dumps(p_value_erdos))

    #calculate p_value of switched graphs
    p_value_switched =  {l: {}  for l in dataSwitched.keys()}
    for lang in dataSwitched.keys():
        num_success=0
        for i in range(len(dataSwitched[lang].values())):
            if(dataC[lang]>= dataSwitched[lang][str(i)]):
                num_success+=1
        p_value_switched[lang]=(num_success/len(dataSwitched[lang].values()))
    with open('output/p_value_switched.json', 'w') as f:
        f.write(json.dumps(p_value_switched))

        
    print(num_success)


    

def main():
    # calc_lang_c_s()

   # for ordering in ['random', 'degree_asc', 'degree_desc', None]:
       # c_t_after_percentage(ordering)
    #p_tests()
    # closeness_SM=[]
    # dict,arr=closeness_normal_graph(adjacency_matrices)
    # np.savetxt('closeness_arr.csv', arr, delimiter=',')
    # np.savetxt('closeness_dict.csv', dict, delimiter=',')
    p_value()



if __name__ == "__main__":
    main()

