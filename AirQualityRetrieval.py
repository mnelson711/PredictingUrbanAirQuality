#This file will scrape the air quality for each city into a csv

from time import sleep
import requests
import csv
import pandas as pd
import json

def retrieveDataByCity(city, state_code, county_code):
    json_object_list = []
    for i in range(1960, 2023):
        url = "https://aqs.epa.gov/data/api/sampleData/byCounty?email=mnelson3@students.stonehill.edu&key=russetfox26&param=42401&bdate=" + str(i) + "0101&edate=" + str(i) + "1231&state=" + state_code + "&county=" + county_code
        with requests.Session() as s:
            response = requests.get(url)
            if response.status_code == 200:
                decoded_content = response.content.decode("utf-8")
                json_object = json.loads(decoded_content)
                
                json_object_list.append(json_object)
                print('success for ' + city)
                print(response)
            
            else:
                print(f"API request for {url} failed with status code: {response.status_code}")
                if response.status_code == 429 or response.status_code == 400:
                    print(f"Waiting 15 seconds before trying again")
                    sleep(15)

    df = pd.json_normalize(json_object_list, "Data")
    df.to_csv('air_quality_data_' + city + '.csv', index=False)
    
##Cities 
retrieveDataByCity('Boston', '25', '025')
retrieveDataByCity('New_York', '36', '061')
retrieveDataByCity('Los_Angeles', '06', '019')
retrieveDataByCity('Bakersfield', '06', '029')
retrieveDataByCity('Visalia', '06', '107')
retrieveDataByCity('Phoenix', '04', '013')
retrieveDataByCity('Denver', '08', '031')
retrieveDataByCity('Sacramento', '06', '034')
retrieveDataByCity('Fresno', '06', '010')
retrieveDataByCity('Reno', '32', '031')