import sqlite3
from random import randint, choice


def createScenarioDB():
    conn = sqlite3.connect('dbs/scenario.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE scenario
                 (id INTEGER PRIMARY KEY, city1 TEXT, city2 TEXT, difficulty_score INTEGER)''')
    conn.commit()
    conn.close()


def calculateDifficultyScore(distance, weather):
    passenger_count = randint(100, 400)
    weather_score = 0
    if weather == "Clear":
        weather_score = 0
    elif weather == "Clouds":
        weather_score = 2
    elif weather == "Drizzle":
        weather_score = 3
    elif weather == "Fog":
        weather_score = 4
    elif weather == "Haze":
        weather_score = 5
    elif weather == "Mist":
        weather_score = 6
    elif weather == "Rain":
        weather_score = 7
    elif weather == "Smoke":
        weather_score = 8
    elif weather == "Snow":
        weather_score = 9
    elif weather == "Thunderstorm":
        weather_score = 10

    return round(distance / passenger_count) + weather_score


def writeScenario():
    conn = sqlite3.connect('dbs/distances.db')
    c = conn.cursor()
    c.execute('SELECT * FROM distances')
    distances = c.fetchall()
    conn.close()

    conn = sqlite3.connect('dbs/scenario.db')
    c = conn.cursor()
    for i in range(100):
        distance = choice(distances)
        difficulty_score = calculateDifficultyScore(distance[2], distance[3])
        c.execute('INSERT INTO scenario VALUES (?, ?, ?, ?)', (i + 1, distance[0], distance[1], difficulty_score))

    conn.commit()
    conn.close()