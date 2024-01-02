from getCities import *
from getCoordinates import *
from getDistance import *
from getScenario import *
import os


def main():
    if not os.path.exists("dbs/cities.db"):
        createCitiesDB()
        cities = getCities()
        writeCities(cities)

    if not os.path.exists("dbs/coordinates.db"):
        createCoordinatesDB()
        calculateCoordinates()

    if not os.path.exists("dbs/distances.db"):
        createDistancesDB()
        writeDistances()

    if not os.path.exists("dbs/scenario.db"):
        createScenarioDB()
        writeScenario()


if __name__ == '__main__':
    main()
