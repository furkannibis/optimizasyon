from getCities import *
from getCoordinates import *
from getDistance import *
from getScenario import *
from getNodeMap import *
from dijstraAlgoritm import *
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

    if not os.path.exists("media/node_map.png"):
        getNodeMap()

    if not os.path.exists("media/result.png"):
        scenario = readScenarioDB()
        createNodes(scenario)


if __name__ == '__main__':
    main()
