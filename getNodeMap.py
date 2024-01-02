import networkx as nx
import matplotlib.pyplot as plt
import sqlite3


def getNodeMap():
    print("Node map çiziliyor...")
    conn = sqlite3.connect('dbs/scenario.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scenario')
    scenario = c.fetchall()
    conn.close()

    G = nx.Graph()
    for i in scenario:
        G.add_edge(i[1], i[2], weight=i[3])

    pos = nx.spring_layout(G, k=2.0)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.savefig("media/node_map.png")

    print("Node map çizildi.")
