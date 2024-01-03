#! /usr/bin/env python3

# Ekstra dosyaları ve os modülünü çalıştırmak için import ediyoruz.
from getCities import *
from getCoordinates import *
from getDistance import *
from getScenario import *
from getNodeMap import *
from dijstraAlgoritm import *
import os


# Veritabanlarını oluşturmak için fonksiyonlarımızı çağırıyoruz.
def main():
    # Burada mantık şu şekilde çalışıyor. Eğer veritabanı ya da gerekli dosya yoksa oluşturacak fonksiyonu çağırıyoruz.

    # Şehirler veritabanı önemli proje buradan başlıyor.
    # Gidilebilecek şehirlerin ne olduğu belirlemek için şehirler veritabanı oluşturuluyor.
    # Bu veritabanının içerisine dünyadaki tüm başkentlerin isimleri yazılıyor.
    if not os.path.exists("dbs/cities.db"):
        createCitiesDB()
        cities = getCities()
        writeCities(cities)

    # Koordinatlar veritabanı şehirlerin koordinatlarını tutmak için oluşturuluyor.
    # Bu veritabanının içerisine şehirlerin koordinatları yazılıyor.
    # Bu koordinatlar sayesinde şehirler arası mesafeler hesaplanıyor.
    # Ayrıca şehirler arası hava durumları da rastgele olacak şekilde bu veritabanına yazılıyor.
    if not os.path.exists("dbs/coordinates.db"):
        createCoordinatesDB()
        calculateCoordinates()

    # Mesafeler veritabanı şehirler arası mesafeleri tutmak için oluşturuluyor.
    # Bu veritabanının içerisine şehirler arası mesafeler yazılıyor.
    # Bu mesafeleri senaryo oluşturmak için kullanıyoruz.
    if not os.path.exists("dbs/distances.db"):
        createDistancesDB()
        writeDistances()

    # Senaryo veritabanı senaryo oluşturmak için oluşturuluyor.
    # Bu veritabanının içerisine senaryo yazılıyor.
    # Senaryodan kastımız kullanıcının girdiği sayı kadar uçuş planı ve rastgele bu uçuş planları için rastgele yolcu sayısı belirleniyor.
    # Şu kadar kişi şuradan şuraya uçacak gibi.
    if not os.path.exists("dbs/scenario.db"):
        createScenarioDB()
        writeScenario()

    # Sırf şekil olsun diye optimizasyondan önce gidilmesi gereken şehirlerin haritasını çiziyoruz.
    # Burada önemli olan kısım optimizasyondan önce gerekli uçak sayısını vermesi.
    if not os.path.exists("media/node_map.png"):
        getNodeMap()

    # Optimizasyon algoritması çalıştırılıyor.
    # Burada dijstra algoritması kullanılıyor.
    # Bu algoritmaya göre zaten üzerinden geçilecek şehirler arası ayrı bir uçak ayarlamaktansa zaten geçecek olan bir uçak bu noktalar için ayarlanıyor.
    if not os.path.exists("media/dijstra_map.png"):
        dijstraAlgoMap()


if __name__ == '__main__':
    main()
