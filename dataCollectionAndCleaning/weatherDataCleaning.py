# collection of scripts for cleaning weather data
import os
import csv
import pandas as pd


# converts the temperature from Kelvin to Celsius
def convert_kelvin(input_file, output_file):
    df = pd.read_csv(input_file)
    kelvin_to_celsius = lambda k: k - 273.15
    df['temp'] = df['temp'].apply(kelvin_to_celsius)
    df.to_csv(output_file, index=False)

# removes column from csv
def remove_column(input_file, output_file, column_name):
    df = pd.read_csv(input_file)
    df = df.drop(column_name, axis=1)
    df.to_csv(output_file, index=False)

# columns wind_gust,rain_1h,rain_3h,snow_1h,snow_3h impute with 0
def impute_zeros(input_file, output_file):
    df = pd.read_csv(input_file)
    df['wind_gust'] = df['wind_gust'].fillna(0)
    df['rain_1h'] = df['rain_1h'].fillna(0)
    df['rain_3h'] = df['rain_3h'].fillna(0)
    df['snow_1h'] = df['snow_1h'].fillna(0)
    df['snow_3h'] = df['snow_3h'].fillna(0)
    df.to_csv(output_file, index=False)

# converts dt_iso column to year, month, day, time columns Ex. 1979-01-01 00:00:00 to 1979, 01, 01, 00:00:00
def convert_date(input_file, output_file):
    df = pd.read_csv(input_file)
    df['year'] = df['dt_iso'].apply(lambda x: x[:4])
    df['month'] = df['dt_iso'].apply(lambda x: x[5:7])
    df['day'] = df['dt_iso'].apply(lambda x: x[8:10])
    df['time'] = df['dt_iso'].apply(lambda x: x[11:])
    df.to_csv(output_file, index=False)

# In visibility column, imputes with last known value
def impute_visibility(input_file, output_file):
    df = pd.read_csv(input_file)
    df['visibility'] = df['visibility'].fillna(method='ffill')
    df.to_csv(output_file, index=False)
    
import pandas as pd

def split_csv_by_city(input_csv_path, output_dir):
    """
    Splits a CSV file into multiple CSV files based on the 'city_name' column.
    
    Parameters:
        input_csv_path (str): The path to the input CSV file.
        output_dir (str): The directory where the output CSV files will be saved.
    """
    df = pd.read_csv(input_csv_path)
    
    for city in df['city_name'].unique():
        city_df = df[df['city_name'] == city]
        output_csv_path = f"{output_dir}/{city.replace(' ', '_').replace('/', '_')}.csv"
        
        city_df.to_csv(output_csv_path, index=False)
        print(f"Saved {output_csv_path}")

# Example usage:
# split_csv_by_city('path_to_your_large_csv.csv', 'output_directory_path')


if __name__ == "__main__":
# split_csv_by_city('../csv/all_cities.csv', '../csv/')
    cities = ['Bakersfield','Los_Angeles','New_York','Phoenix','Reno','Visalia']
    
    
    for city in cities:
        input_file = "csv/" + city + ".csv"
        output_file = "csv/weather_data_" + city + ".csv"
        columns_to_remove = ['dt_iso', 'timezone', 'sea_level','grnd_level', 'weather_icon']
        convert_kelvin(input_file, output_file)
        impute_zeros(output_file, output_file)
        impute_visibility(output_file, output_file)
        convert_date(output_file, output_file)
        for column in columns_to_remove:
            remove_column(output_file, output_file, column)

