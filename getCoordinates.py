import geopy
import sqlite3
from tqdm import tqdm


def createCoordinatesDB():
    print("Koordinat veritabanı oluşturuluyor...")
    conn = sqlite3.connect('dbs/coordinates.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS coordinates (city text, latitude real, longitude real)')
    conn.commit()
    conn.close()
    print("Koordinat veritabanı oluşturuldu.")


def calculateCoordinates():
    conn = sqlite3.connect('dbs/cities.db')
    c = conn.cursor()
    cities = c.execute('SELECT * FROM cities').fetchall()
    conn.close()

    conn = sqlite3.connect('dbs/coordinates.db')
    c = conn.cursor()
    for city in tqdm(desc="Koordinatlar hesaplanıyor", iterable=cities):
        try:
            geolocator = geopy.Nominatim(user_agent="myApp")
            location = geolocator.geocode(city[0])
            c.execute('INSERT INTO coordinates VALUES (?, ?, ?)', (city[0], location.latitude, location.longitude))
        except:
            print("Koordinatlar hesaplanırken hata oluştu: " + city[0])
    conn.commit()
    conn.close()
    print("Koordinatlar hesaplandı.")
