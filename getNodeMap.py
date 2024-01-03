import networkx as nx
import matplotlib.pyplot as plt
import sqlite3

# Şimdi geldik zurnanın zırt dediği yere!!!
# Bu kısımda optimizasyondan önce gidilecek şehirlerin haritasını çiziyoruz.
# Bunun için networkx ve matplotlib kütüphanelerini kullanıyoruz.

def getNodeMap():
    print("Node map çiziliyor...")

    # İlk başta senaryo veritabanından gidilecek şehirleri çekiyoruz.
    conn = sqlite3.connect('dbs/scenario.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scenario')
    scenario = c.fetchall()
    conn.close()

    # Şimdi gidilecek şehirlerin haritasını çiziyoruz.
    # G'den kastım Graph yani grafik.
    G = nx.DiGraph()
    planeNumber = 0
    for i in scenario:

        # Gidilecek şehirlerin hepsini şuradan şuraya gidecek diye haritaya ekliyoruz.
        G.add_edge(i[1], i[2])

        # Her bir uçuş için uçak sayısını bir arttırıyoruz.
        planeNumber += 1

    # Burası haritanın şekli için
    pos = nx.spring_layout(G, k=10.0)

    # Burada haritayı çiz artık demek.
    nx.draw(G, pos, with_labels=True, font_weight='light')
    plt.savefig("media/node_map.png")

    print("Node map çizildi.")
    print("Optimizasyondan önce gerekli uçak sayısı: ", planeNumber)
