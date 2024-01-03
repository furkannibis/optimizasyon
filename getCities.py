from bs4 import BeautifulSoup
import requests
import sqlite3
from tqdm import tqdm


# Şehirleri bu websitesiden çekiyoruz.
# https://en.wikipedia.org/wiki/List_of_national_capitals
# Burada web kazıma işlemi dönüyor kısaca.
def getCities():
    url = 'https://en.wikipedia.org/wiki/List_of_national_capitals'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.findAll('tbody')

    cityRow = table[1].findAll('tr')
    cities = []
    for row in cityRow:
        city = row.findAll('td')
        if len(city) > 0:
            cities.append(city[0].find('a').text.strip())

    return cities

# Şehirler veritabanı burada oluşturuluyor.
# Veritabanı olarak sqlite3'ü kullanıyoruz.
def createCitiesDB():
    print("Şehir veritabanı oluşturuluyor...")
    conn = sqlite3.connect('dbs/cities.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cities (city text)')
    conn.commit()
    conn.close()
    print("Şehir veritabanı oluşturuldu.")

# Oluşturduğumuz veritabanına şehirleri yazıyoruz.
# Buralarda çok bir şey yok zaten.
def writeCities(cities):
    conn = sqlite3.connect('dbs/cities.db')
    c = conn.cursor()
    for city in tqdm(desc="Şehirler veritabanına aktarılıyor", iterable=cities):
        c.execute('INSERT INTO cities VALUES (?)', (city,))
    conn.commit()
    conn.close()
    print("Şehirler veritabanına aktarıldı.")
