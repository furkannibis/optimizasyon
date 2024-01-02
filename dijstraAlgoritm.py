import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import sqlite3
from random import choice


def readScenarioDB():
    conn = sqlite3.connect('dbs/scenario.db')
    c = conn.cursor()
    c.execute("SELECT * FROM scenario")
    scenario = c.fetchall()
    conn.close()
    return scenario


def createNodes(scenario):
    G = nx.Graph()
    for i in scenario:
        G.add_edge(i[1], i[2], weight=i[3])

    notUsedCities = list(G.nodes)
    resultGraph = nx.Graph()

    while len(notUsedCities) > 0:
        selectedCity = choice(notUsedCities)
        print(f"Seçilen başlangıç şehri: {selectedCity}")
        resultGraph.add_node(selectedCity, color="red")

        notUsedCities.remove(selectedCity)

        path = nx.single_source_dijkstra_path_length(G, selectedCity)
        path_nodes = list(path.keys())
        path_values = list(path.values())

        for i in range(len(path_nodes)):
            try:
                resultGraph.add_edge(path_nodes[i], path_nodes[i + 1], weight=path_values[i + 1])
                notUsedCities.remove(path_nodes[i + 1])
                print(path_nodes[i], path_nodes[i + 1], path_values[i + 1])
            except IndexError:
                resultGraph.add_node(path_nodes[i])
                print(path_nodes[i])
                print("\n\n")

    pos = nx.spring_layout(resultGraph, k=2.0)
    nx.draw(resultGraph, pos, with_labels=True, font_weight='bold')
    plt.savefig("media/result.png")
