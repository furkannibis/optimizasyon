import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt
import sqlite3
from random import choice

# Hazır mısın zortlamaya !!!


# Öncelikle tüm uğranılacak şehirleri çekiyoruz.
# Dikkat et burada şehirlerin tekrar etmemesi için set() kullanıyoruz.
# Set() kullanmazsak aynı şehirler tekrar tekrar ekleniyor.
# Amaç burada sadece hangi şehirlerde işimiz olacak onu belirlemek.
def getAllCity():
    conn = sqlite3.connect("dbs/scenario.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scenario")
    scenario = c.fetchall()
    conn.close()

    cities = []
    for i in scenario:
        cities.append(i[1])
        cities.append(i[2])

    return list(set(cities))

# Burada kalkış için kullanılacak şehirler belirleniyor.
# Burada mantık şu şekilde çalışıyor.
# Senaryo veritabanından yalnızca city1 sütununu çekiyoruz.
def departurePoint():
    conn = sqlite3.connect("dbs/scenario.db")
    c = conn.cursor()
    c.execute("SELECT city1 FROM scenario")
    scenario = c.fetchall()
    conn.close()

    return [x[0] for x in scenario]

# Şimdi algoritma kısmına geldik
def dijstraAlgoMap():

    # Şehirlerin hepsini çekiyoruz.
    # Bu şehirleri haritaya ekliyoruz ancak aralarında bağlantı yok. Yalnızca şehirler var.
    G = nx.DiGraph()
    for city in getAllCity():
        G.add_node(city)

    # Şimdi senaryo veritabanından kalkış ve iniş şehirlerini alıyoruz.
    conn = sqlite3.connect("dbs/scenario.db")
    c = conn.cursor()
    c.execute("SELECT * FROM scenario")
    scenario = c.fetchall()
    conn.close()

    # Şehirler arası bağlantıyı yapıyoruz.
    # weight parametresi aralarındaki zorluk puanını belirtiyor. Bunu önceden hesaplamıştık.
    for i in scenario:
        G.add_edge(i[1], i[2], weight=i[3])

    # Şimdi optimizasyon için boş bir grafik oluşturuyoruz.
    resultGraph = nx.DiGraph()
    planeNumber = 0


    # Şimdi düşün bakalım.
    # Sonuçta kalkış şehirleri bizim için önemli
    # Çünkü bir şehir'e sadece yolcu bırakılacak ve o şehirden başka bir yere gidilmeyecekse döngü bitmiş demek oluyor zaten.
    # O yüzden kalkış şehirlerini geziyoruz.
    for i in departurePoint():
        # Şimdi tüm kalkış şehirlerinin diğer şehirlere olan dijstra yolunu çekiyoruz.
        # Bunu networkx kütüphanesi ile yapıyoruz. Otomatik yapıyor sağolsun canım benim.
        path = nx.single_source_dijkstra_path(G, i)

        # Burası çokomelli.
        # Şimdi mantık şu
        # Bir şehirden bir şehre oradan da gidebileceğin 2 adet şehir oluyor ise burada ekstra bir uçak daha ayarlamak gerekiyor.
        # Ama öncesi için bir uçak yeterli gibi.
        # Anlamadıysan sorun yok ben de anlamadım.
        # Ama çalışıyor.

        for x in range(1, len(list(path.values())) + 1):

            # Şimdi burada son dijstra yolunu alıyoruz. ve bu yol zaten var mı kontrol ediyoruz.
            # Çünkü eğer varsa gerek yok kullanmaya.
            # Zaten algoritma burada
            # Ama eğer yoksa onu da ekliyoruz.
            if (list(path.values())[-x]) not in resultGraph:
                for j in range(0, len(list(path.values())[-x])):
                    try:
                        # Yine bir kontrol yapıyoruz.
                        # Eğer zaten varsa eklemiyoruz.
                        if list(path.values())[-x][j] not in resultGraph:

                            # burada belirli yol ayrımı olduğunu anlamış oluyoruz zaten.
                            # Bu demek ki buradan sonra bir uçağa daha ihtiyacımız var demek.
                            # O yüzden uçak sayısını arttırıyoruz.
                            resultGraph.add_edge(list(path.values())[-x][j], list(path.values())[-x][j + 1])
                            planeNumber += 1

                    # Burada şehir bittiyse hata alıyoruz zaten.
                    # O yüzden hata alırsak except ile hata almamızı engelliyoruz ki proje çalışmaya devam etsin.
                    except:
                        pass

    # Burası haritanın şekli için
    # Kısaca elindeki grafiği oluştur demek. Buraları çok takma.
    pos = nx.spring_layout(resultGraph, k=10.0)
    nx.draw(resultGraph, pos, with_labels=True, font_weight='light')
    plt.savefig("media/dijstra_map.png")
    print("Optimizasyondan sonra gerekli uçak sayısı: ", planeNumber)
