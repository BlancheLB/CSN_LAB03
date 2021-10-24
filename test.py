import random
import math

languages = ['Arabic', 'Basque', 'Catalan', 'Chinese', 'Czech', 'English', 'Greek', 'Hungarian', 'Italian', 'Turkish']
 

sequences_matrices=[]
nodes=[]
for lang in languages:
    graph_file = open('dependency_networks/' + lang + "_syntactic_dependency_network.txt",encoding='UTF8')
    count = 0
    index=0
    nodes=[]
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
            if index==0:
                nodes.append(words)
                index +=1
            elif nodes[index-1][0]==words[0]:
                nodes[index-1][1].append(words[1])
            else:
                index +=1
                nodes.append([words[0],[words[1]]])
    sequences_matrices.append([lang,nodes])
    
#print(sequences_matrices[5])




def switching_model(mat,Q,E):
    n=Q*E;
    for i in range(n):
        #index of two random nodes to exchange edge
        index1=random.randint(1,len(mat)-1)
        index2=random.randint(1,len(mat)-1)
        #index of two nodes to exchange edge
        i1=random.randint(0,len(mat[index1][1])-1)
        i2=random.randint(0,len(mat[index2][1])-1)
        
        mat[index1][1].insert(i2,mat[index1][1][i1])
        mat[index2][1].insert(i1,mat[index1][1][i2])
        mat[index1][1].pop(i1+1)
        mat[index2][1].pop(i2+1)
    return mat
       
def switchM_all(mat_languages):
    for i in range(mat_languages):
        E=mat_languages[i][0][1]
        Q=math.log(E)
        switching_model(mat_languages[i][1],Q,E)
    return mat_languages



def switching_model(dict,Q,E):
    n=int(Q*E);
    for i in range(n):
        #index of two random nodes to exchange edge
        index1=random.randint(1,len(mat)-1)
        index2=random.randint(1,len(mat)-1)
        
        mat[index1][1],mat[index2][1]=mat[index2][1],mat[index1][1]
    return mat





def switching_model(mat,Q,E):
    n=Q*E;
    for i in range(n):
        #index of two random nodes to exchange edge
        index1=random.randint(1,len(mat)-1)
        index2=random.randint(1,len(mat)-1)
        #index of two nodes to exchange edge
        i1=random.randint(0,len(mat[index1][1])-1)
        i2=random.randint(0,len(mat[index2][1])-1)
        print("mat index 1 avant ",mat[index1])
        print("mot à échanger 1",mat[index1][1][i1])
        print("mat index 2 avant ",mat[index2])
        print("mot à échanger 2",mat[index2][1][i2])

        mat[index1][1].insert(i2,mat[index1][1][i1])
        mat[index2][1].insert(i1,mat[index1][1][i2])
        mat[index1][1].pop(i1+1)
        mat[index2][1].pop(i2+1)
        print("mat index 1 apres ",mat[index1])
        print("mat index 2 apres ",mat[index2])

switching_model(sequences_matrices[5][1],1,1)
print(sequences_matrices[5])