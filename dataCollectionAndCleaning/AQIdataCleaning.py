#This file will clean the AQI data
import pandas as pd

def removeMissingRows(df, column_name):
    df = df.dropna(subset=[column_name])
    return df

def dropFeatures(df, features):
    for feature in features:
        df.drop(feature, axis=1, inplace=True)
        print('dropped column: ', feature)
    return df

def createNewDate(df):
    df['date_gmt'] = pd.to_datetime(df['date_gmt'], errors='coerce')
    df['year'] = df['date_gmt'].dt.year
    df['month'] = df['date_gmt'].dt.month
    df['day'] = df['date_gmt'].dt.day
    df = df.drop(columns=['date_gmt'])
    return df

def calculate_aqi(pollutant, concentration, units):
    #calculate aqi given a pollutant and the concentration.
    #note for this sata set i've only seen sulfur dioxide so far but who knows.
    pollutant_breakpoints = {
        'pm25': [(0, 12.0, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200),(150.5, 250.4, 201, 300), (250.5, 350.4, 301, 400), (350.5, 500.4, 401, 500)],
        'pm10': [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200),(355, 424, 201, 300), (425, 504, 301, 400), (505, 604, 401, 500)],
        'o3':   [(0, 54, 0, 50), (55, 70, 51, 100), (71, 85, 101, 150), (86, 105, 151, 200),(106, 200, 201, 300), (201, 504, 301, 400)],
        'sulfur dioxide':  [(0, 35, 0, 50), (36, 75, 51, 100), (76, 185, 101, 150), (186, 304, 151, 200),(305, 604, 201, 300), (605, 1004, 301, 400), (1005, 1604, 401, 500)],
        'no2':  [(0, 53, 0, 50), (54, 100, 51, 100), (101, 360, 101, 150), (361, 649, 151, 200), (650, 1249, 201, 300), (1250, 2049, 301, 400), (2050, 4049, 401, 500)],
        'co':   [(0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300), (30.5, 50.4, 301, 400), (50.5, 604, 401, 500)],
    }

    # getting breakpoints for specific pollutant
    breakpoints = pollutant_breakpoints.get(pollutant.lower())
    if not breakpoints:
        raise ValueError(f"Unsupported pollutant: {pollutant}")

    # get the range measurement falls in
    concentration = abs(concentration)
    for low, high, aqi_low, aqi_high in breakpoints:
        if low <= concentration <= high:
            break
    else:
        raise ValueError(f"Concentration {concentration} {units} is outside valid range for {pollutant}")

    #this is AQI formula
    aqi = round(((aqi_high - aqi_low) / (high - low)) * (concentration - low) + aqi_low)

    return aqi

def impute_aqi(df):
    #this function created a new aqi column based on parameter and sample measurement columns
    if 'sample_measurement' not in df.columns or 'parameter' not in df.columns:
        raise ValueError("DataFrame must contain 'sample_measurement' and 'parameter' columns.")

    #calculate aqi for each row
    def calculate_row_aqi(row):
        try:
            aqi = calculate_aqi(row['parameter'], row['sample_measurement'], 'ppb')
            return aqi
        except ValueError as e:
            print(f"Error calculating AQI for row {row.name}: {e}")
            return None

    df['aqi'] = df.apply(calculate_row_aqi, axis=1)
    return df






def clean_file(filename,cityname):
    #fucntion to preform all changes on data and create new csv file
    file = pd.read_csv(filename, low_memory=False)
    # print(file['parameter'].unique())
    cleaned_df = file
    features_to_drop = ['site_number', 'datum', 'sample_duration_code', 'date_local', 'time_local', 'date_of_last_change','cbsa_code']
    cleaned_df = createNewDate(file)
    cleaned_df = dropFeatures(cleaned_df, features_to_drop)
    cleaned_df = removeMissingRows(cleaned_df, 'sample_measurement')
    cleaned_df = impute_aqi(cleaned_df)
    cleaned_df.to_csv('aqi_cleaned_'+ cityname +'.csv', index=False)

if __name__ == "__main__":
    cities = ['Bakersfield','Los_Angeles','New_York','Phoenix','Reno','Visalia','Denver']
    for city in cities:
        filename = "csv/air_quality_data_" + city +".csv"
        clean_file(filename, city)