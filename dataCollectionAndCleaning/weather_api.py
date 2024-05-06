import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import time


def get_weather_data(lat, lon, api_key):
    end_date = datetime(1980, 1, 1)
    start_date = datetime.now()

    start_epoch = int(start_date.timestamp())
    end_epoch = int(end_date.timestamp())
    current_epoch = start_epoch
    data = []
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&start=631187388&end=631273788type=hour&appid={api_key}"
    response = requests.get(url)
    data.append(response)
    # attempts = 0
    # while current_epoch >= end_epoch:
    #     current_date = datetime.fromtimestamp(current_epoch)
    #     next_date = current_date - timedelta(days=1)
    #     next_epoch = int(next_date.timestamp())
    #     url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&start={next_epoch}&end={current_epoch}type=hour&appid={api_key}"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         if current_epoch % 100000 == 0:
    #             os.system('cls') 
    #             print("|"*current_epoch/10000000, end="")
    #         data.append(response)
    #         current_epoch = next_epoch
    #     else:
    #         attempts += 1
    #         print(str(response.status_code) + " " + response.text + "\n" + url)
    #         print(f"attempt {attempts} failed, retrying in {attempts * 2} seconds")
    #         time.sleep(attempts * 2)
    #         if attempts > 2:
    #             attempts = 0
    #             current_epoch = next_epoch
    return data


def get_location_data(location, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def main():
    locations = [
        "New York",
        "Los Angeles",
        "Fresno",
        "Sacramento",
        "Denver",
        "Visalia",
        "Bakersfield",
        "Reno",
    ]
    longitude_and_latitudes = {}
    with open("key") as file:
        api_key = file.read()
    print("got api key")

    for location in locations:
        long_lat = get_location_data(location, api_key)
        long_lat = long_lat[0]
        longitude_and_latitudes[location] = long_lat["lat"], long_lat["lon"]
    print(longitude_and_latitudes)

    for city, long_lat in longitude_and_latitudes.items():
        print(f"getting weather data for {city}")
        weather_data = get_weather_data(long_lat[0], long_lat[1], api_key)
        # daily_weather = weather_data["daily"]
        path = os.path.join("data", "weather_data", f"{city}_weather.json")
        f = open(path, "a")
        for data in weather_data:
            f.write(json.dumps(data.json()))
        # df = pd.read_json(weather_data)
        # df.to_csv(f'{city}_weather.csv', index=False)


main()
