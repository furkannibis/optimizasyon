from bs4 import BeautifulSoup
import requests


def getCities():
    url = 'https://en.wikipedia.org/wiki/List_of_national_capitals'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.findAll('tbody')
    print(len(table))
    print(table[1].prettify())

    getCity = table[1].findAll('a')
    cities = [city.text for city in getCity if city.get('title') is not None]
    return cities
