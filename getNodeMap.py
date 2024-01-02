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

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=10)
    nx.draw_networkx_edges(G, pos, width=0.5)
    nx.draw_networkx_labels(G, pos, font_size=5, font_family="sans-serif")
    plt.axis("off")
    plt.savefig("media/node_map.png", dpi=1000)
    print("Node map çizildi.")
