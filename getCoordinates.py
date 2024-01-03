import geopy
import sqlite3
from tqdm import tqdm


# Burada şehirlerin koordinatlarını yazacağımız veritabanını oluşturuyoruz.
# Bir önceki kısımla neredeyse aynı zaten çok bir fark yok
def createCoordinatesDB():
    print("Koordinat veritabanı oluşturuluyor...")
    conn = sqlite3.connect('dbs/coordinates.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS coordinates (city text, latitude real, longitude real)')
    conn.commit()
    conn.close()
    print("Koordinat veritabanı oluşturuldu.")

# Burada işler biraz karışmaya başlıyor.
# Şehirlerin koordinatlarını almak için geopy kütüphanesinin Nominatim fonksiyonunu kullanıyoruz.
# Bu fonksiyon şehrin adını alıyor ve bize o şehrin koordinatlarını veriyor.
# Aldığımız bu koordinatları veritabanına yazıyoruz.
def calculateCoordinates():
    # İlk başta şehirlerin isimlerini alıyoruz şehirler veritabanından.
    conn = sqlite3.connect('dbs/cities.db')
    c = conn.cursor()
    cities = c.execute('SELECT * FROM cities').fetchall()
    conn.close()

    # Şehirlerin koordinatlarını yazacağımız veritabanına bağlanıyoruz.
    conn = sqlite3.connect('dbs/coordinates.db')
    c = conn.cursor()
    for city in tqdm(desc="Koordinatlar hesaplanıyor", iterable=cities):
        try:
            # Burada şehirlerin koordinatlarını hesaplıyoruz.
            # geopy bunu direkt yapıyor bize zaten.
            geolocator = geopy.Nominatim(user_agent="myApp")
            location = geolocator.geocode(city[0])
            c.execute('INSERT INTO coordinates VALUES (?, ?, ?)', (city[0], location.latitude, location.longitude))
        except:
            # Nolur nolmaz diye hata yakalıyoruz.
            print("Koordinatlar hesaplanırken hata oluştu: " + city[0])
    conn.commit()
    conn.close()
    print("Koordinatlar hesaplandı.")
