from getCities import *
from getCoordinates import *
import os


def main():
    if not os.path.exists("dbs/cities.db"):
        createCitiesDB()
        cities = getCities()
        writeCities(cities)

    if not os.path.exists("dbs/coordinates.db"):
        createCoordinatesDB()
        calculateCoordinates()

if __name__ == '__main__':
    main()