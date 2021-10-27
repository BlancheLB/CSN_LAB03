import json
import matplotlib.pyplot as plt

def plotcs_full():
    with open('output/language_c_s_full.json','r') as f:
        data = json.load(f)
    
    fig = plt.figure()
    # ax = fig.add_axes([0,0,1,1])
    plt.bar(data.keys(), data.values(), color='darkblue')
    plt.xlabel('Language')
    plt.ylabel('Closeness centrality')
    plt.title('Closeness centrality per language graph')
    plt.xticks(rotation=25)
    plt.show()
    # print(data)

def plot_percentage_and_sorting():
    fig = plt.figure()
    for ordering in ['random', 'degree_asc', 'degree_desc', 'normal']:
        with open('output/percentages_c_s' + ordering + '.json','r') as f:
            data = json.load(f)
        plt.plot([0.05 * k for k in range(1,21)], data.values(), label=ordering + ' ordering')
    plt.plot([0,1], [0.3326981570252918, 0.3326981570252918], label="correct result")
    plt.xlabel('Percentage of the nodes processed')
    plt.ylabel('Graph closeness centrality')
    plt.title('Closeness centrality over processing time,\n with different orderings (English)')
    plt.legend()
    plt.show()

def plot_percetage_all():

    with open('output/language_c_s_full.json', 'r') as f:
        ccs = json.load(f)

    fig, axs = plt.subplots(2, 2)
    orderings = ['random', 'degree_asc', 'degree_desc', 'normal']
    for j in [i for i in range(0,4)]:
        with open('output/percentages_c_s' + orderings[j] + '.json','r') as f:
            data = json.load(f)
        plot = axs[j//2, j%2]
        for key,val in data.items():
            plot.plot([0.005 * k for k in range(1,12)], [ccs[key] - v for v in val.values()][0:11], label=key)
        plot.set(xlabel='Percentage of the nodes processed', ylabel='Difference with real closeness centrality')
        plot.set_title(orderings[j] + ' ordering')
    fig.suptitle('Closeness centrality correctness for small measurements')
    plt.legend()
    plt.show()

def plot_measurements_erdos():
    with open('./output/ptest_erdos.json','r') as f:
        data = json.load(f)
    barWidth=0.25
    groupBarWidth = barWidth * 20 + 2
    count=0
    languages = ['Basque', 'Greek',  'Turkish']
    for i in range(len(data.keys())):
        for j in range(20):
            val = data[languages[i]][str(j)]
            plt.bar(i*groupBarWidth + j*barWidth,val, width=barWidth)

        
    plt.xticks([2.5,9,17],languages)
    plt.ylabel('Closeness centrality')
    plt.title('Closenness centrality of Erdos graphs per languages')
    plt.show()

def plot_measurements_switching():
    with open('./output/ptest_switched.json','r') as f:
        data = json.load(f)
    barWidth=0.25
    groupBarWidth = barWidth * 20 + 2
    count=0
    languages = ['Basque', 'Greek',  'Turkish']
    for i in range(len(data.keys())):
        for j in range(20):
            val = data[languages[i]][str(j)]
            plt.bar(i*groupBarWidth + j*barWidth,val, width=barWidth)
        
    plt.xticks([2.5,9,17],languages)
    plt.ylabel('Closeness centrality')
    plt.title('Closenness centrality of switched graphs per languages')
    plt.show()

def main():
    # plotcs_full()
    #plot_percentage_and_sorting()
    plot_measurements_erdos()
    #plot_measurements_switching()


if __name__ == "__main__":
    main()