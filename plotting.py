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
        #plt.xticks([i + 7 for i in range(len(data.keys()))],languages[i])
    
    plt.xlabel('Graph', fontweight='bold')
    plt.xticks([i + 7 for i in range(len(data.keys()))],languages)
    plt.ylabel('Closeness centrality')
    plt.title('Closenness centrality with a Erdos graph per languages')
    plt.show()

def main():
    # plotcs_full()
    #plot_percentage_and_sorting()
    plot_measurements_erdos()


if __name__ == "__main__":
    main()