"""
Authors: Blanche Le Boniec & Jorik van Nielen
"""



# load in the files and make adjacency lists
languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
adjacency_matrices = {}
for lang in languages:
    graph_file = open('dependency_networks/' + lang + "_syntactic_dependency_network.txt")
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
            if words[0] in adjacency_matrix.keys():
                adjacency_matrix[words[0]].append(words[1])
            else:
                adjacency_matrix[words[0]] = [words[1]]    
#print(adjacency_matrices["English"])



