import csv
import json
import requests
import os


def fetch_and_save_data(api_url, csv_filename):

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        result = data.get("result", [])
        if not result:
            result = data.get("co2", [])
        if not result:
            result = data.get("methane", [])
        if not result:
            result = data.get("nitrous", [])
        if not result:
            result = data.get("arcticData", [])
        if api_url == "https://global-warming.org/api/ocean-warming-api":
            result = [
                {"year": year, "value": value}
                for year, value in data.get("result", {}).items()
            ]
            with open(csv_filename, mode="w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["year", "value"])
                writer.writeheader()
                for row in result:
                    writer.writerow(row)
            print(f"Data from {api_url} has been appended to {csv_filename}")
            return

        if not result:
            print(f"No data found in {api_url}")
            return

        fieldnames = list(result[0].keys())

        with open(csv_filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result)

        print(f"Data from {api_url} has been appended to {csv_filename}")

    else:
        print(f"Failed to fetch data from {api_url}")


path = os.path.join(os.getcwd(), "data")

fetch_and_save_data(
    "https://global-warming.org/api/temperature-api",
    os.path.join(path, "temperature_data.csv"),
)
fetch_and_save_data(
    "https://global-warming.org/api/co2-api", os.path.join(path, "co2_data.csv")
)
fetch_and_save_data(
    "https://global-warming.org/api/methane-api", os.path.join(path, "methane_data.csv")
)
fetch_and_save_data(
    "https://global-warming.org/api/nitrous-oxide-api",
    os.path.join(path, "nitrous_data.csv"),
)
fetch_and_save_data(
    "https://global-warming.org/api/arctic-api", os.path.join(path, "arctic_data.csv")
)
fetch_and_save_data(
    "https://global-warming.org/api/ocean-warming-api",
    os.path.join(path, "ocean_warming_data.csv"),
)
