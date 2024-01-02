import sqlite3
from tqdm import tqdm
from geopy.distance import geodesic
from random import choice


def createDistancesDB():
    print("Mesafe veritabanı oluşturuluyor...")
    conn = sqlite3.connect('dbs/distances.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS distances (city1 text, city2 text, distance real, weather TEXT)')
    conn.commit()
    conn.close()
    print("Mesafe veritabanı oluşturuldu.")


def writeDistances():
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
            if i[0] != j[0]:
                distance = round(geodesic((i[1], i[2]), (j[1], j[2])).km, 2)
                c.execute('INSERT INTO distances VALUES (?, ?, ?, ?)', (i[0], j[0], distance, choice(weather)))

    conn.commit()
    conn.close()
