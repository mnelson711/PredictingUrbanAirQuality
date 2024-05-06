import bs4
import requests
import pandas as pd
import os
from zipfile import ZipFile
import logging

url = "https://aqs.epa.gov/aqsweb/airdata/download_files.html"
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, "html.parser")
links = soup.find_all("a")
tags = ["daily_44201", "daily_42401", "daily_42101", "daily_42602"]

for link in links:
    if any(string in link.get("href") for string in tags):
        file_url = link.get("href")

        file_name = os.getcwd() + "/data/" + file_url.split("/")[-1]
        response = requests.get("https://aqs.epa.gov/aqsweb/airdata/" + file_url)

        with open(file_name, "wb") as file:
            file.write(response.content)

        with ZipFile(file_name, "r") as zip_ref:
            zip_ref.extractall(os.getcwd() + "/data/")
            extracted_files = zip_ref.namelist()

        os.remove(file_name)

        for extracted_file in extracted_files:
            if extracted_file.endswith(".csv"):
                csv_file_path = os.path.join(os.getcwd(), "data", extracted_file)
                df = pd.read_csv(csv_file_path)
                columns_to_keep = [
                    "Longitude",
                    "Latitude",
                    "Date Local",
                    "Parameter Name",
                    "AQI",
                ]
                df = df.loc[:, columns_to_keep]
                df[df["Parameter Name"].iloc[0]] = df["AQI"]
                df = df.drop(columns=["Parameter Name", "AQI"])
                with open(os.path.join(os.getcwd(), "data", "AQI.csv"), "a") as f:
                    df.to_csv(f, header=False, index=False)
                logging.info(f"{file_url}csv written to AQI.csv")
                print(f"DataFrame written to AQI.csv")
                os.remove(csv_file_path)


