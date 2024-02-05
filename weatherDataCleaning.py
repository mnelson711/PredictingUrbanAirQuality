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

if __name__ == "__main__":
# loop for all csv files in the directory
    # abs_path = os.path.abspath(os.getcwd())
    # for file in os.listdir("abs_path"):
    #     if file.endswith(".csv"):
    #         print(file)

    input_file = "csv/weather_data_Boston.csv"
    output_file = "csv/weather_data_Boston.csv"
    remove_column(input_file, output_file, "timezone")

