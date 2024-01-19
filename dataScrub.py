#This code will scrub the air quality data from the API and place into a csv

from time import sleep
import requests
import csv
import pandas as pd
import json


# queries are limited to one year at a time. Earliest data point is 1968
json_object_list = []
for i in range(1960, 2023):
    url = "https://aqs.epa.gov/data/api/sampleData/byCounty?email=mnelson3@students.stonehill.edu&key=russetfox26&param=42401&bdate=" + str(i) + "0101&edate=" + str(i) + "1231&state=25&county=027"
    with requests.Session() as s:
        response = requests.get(url)
        if response.status_code == 200:
            decoded_content = response.content.decode("utf-8")
            json_object = json.loads(decoded_content)
            
            json_object_list.append(json_object)
        
        else:
            print(f"API request for {url} failed with status code: {response.status_code}")
            if response.status_code == 429 or response.status_code == 400:
                print(f"Waiting 15 seconds before trying again")
                sleep(15)

df = pd.json_normalize(json_object_list, "Data")
df.to_csv('air_quality_data.csv', index=False)