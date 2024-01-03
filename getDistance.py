import sqlite3
from tqdm import tqdm
from geopy.distance import geodesic
from random import choice

# Yine diğer kısımlarla aynı burada mesafeleri çekeceğimiz veritabanını oluşturuyoruz.
# Burada fark iki şehir arasında bir de hava durumu mevzusu olması.
def createDistancesDB():
    print("Mesafe veritabanı oluşturuluyor...")
    conn = sqlite3.connect('dbs/distances.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS distances (city1 text, city2 text, distance real, weather TEXT)')
    conn.commit()
    conn.close()
    print("Mesafe veritabanı oluşturuldu.")


# Şimdi mesafe veritabanını oluşturduk.
# Ancak bunları zor yoldan da olsa veritabanına yazmamız gerekiyor.

def writeDistances():
    # Hava durumları listesi buradan random seçim yapacağız.
    weather = ["Clear", "Clouds", "Drizzle", "Fog", "Haze", "Mist", "Rain", "Smoke", "Snow", "Thunderstorm"]

    conn = sqlite3.connect('dbs/coordinates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM coordinates')
    coordinates = c.fetchall()
    conn.close()

    conn = sqlite3.connect('dbs/distances.db')
    c = conn.cursor()
    for i in tqdm(desc="Mesafeler veritabanına aktarılıyor", iterable=coordinates):
        for j in coordinates:
            # Bir şehrin kendisine olan mesafesini hesaplamıyoruz.
            if i[0] != j[0]:
                # Mesafe hesaplaması için geopy kütüphanesinin geodesic fonksiyonunu kullanıyoruz.
                # Bu fonksiyon kısaca iki koordinat arasındaki mesafeyi hesaplıyor.
                # Burada mesafeyi kilometre cinsinden hesaplıyoruz.
                distance = round(geodesic((i[1], i[2]), (j[1], j[2])).km, 2)

                # Burada veritabanına yazma işlemini yapıyoruz ancak
                # choice(weather) kısmı rastgele hava durumu seçmek için. Burası önemli çünkü şehirler arası zorluk mesafesini ayarlamada gerekli!
                c.execute('INSERT INTO distances VALUES (?, ?, ?, ?)', (i[0], j[0], distance, choice(weather)))

    conn.commit()
    conn.close()
