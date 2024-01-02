from getCities import *
import os


def main():
    if not os.path.exists("dbs/cities.db"):
        createCitiesDB()
        cities = getCities()
        writeCities(cities)


if __name__ == '__main__':
    main()