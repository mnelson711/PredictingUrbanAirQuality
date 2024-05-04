#This file will join the AQI and Weather Data by time to create one mega, super awesome, computer crashing csv file
import pandas as pd

def joinFiles(air_quality_data, weather_data, cityname):
    #initial cleanup
    weather_data = weather_data.dropna(subset=['time','year', 'month', 'day'])
    air_quality_data = air_quality_data.dropna(subset=['time_gmt','year', 'month', 'day'])
    weather_data['time'] = weather_data['time'].str.slice(0, 5)
    air_quality_data['time'] = air_quality_data['time_gmt']
    merged_data = pd.merge(weather_data, air_quality_data, on=['time','day', 'month', 'year'], how='inner')
    
    #final cleanup
    merged_data.drop_duplicates(inplace=True)
    merged_data.drop(columns=['lat', 'lon','dt'], inplace=True)
    merged_data['aqi'].apply(categorize_aqi)
    # merged_data.drop('time_gmt')
    # merged_data.to_csv("csv/merged_data.csv", index=False)
    print('finished merging for:', cityname)
    return merged_data
    

# Function to categorize AQI
def categorize_aqi(aqi):
    if aqi <= 50:
        return 'Good'
    elif aqi <= 100:
        return 'Moderate'
    elif aqi <= 150:
        return 'Unhealthy for Sensitive Groups'
    elif aqi <= 200:
        return 'Unhealthy'
    elif aqi <= 300:
        return 'Very Unhealthy'
    else:
        return 'Hazardous'
    
def count_unique_values(df, column_name):
    """
    Counts unique values in a specified column of a pandas DataFrame.

    Parameters:
    - df: pandas.DataFrame
    - column_name: str, the name of the column to analyze.

    Returns:
    - A dictionary with unique values as keys and their counts as values.
    """
    if column_name in df.columns:
        unique_counts = df[column_name].value_counts().to_dict()
        return unique_counts
    else:
        return f"Column '{column_name}' not found in DataFrame."


if __name__ == "__main__":
    cities = ['Bakersfield','Los_Angeles','New_York','Phoenix','Reno','Visalia','Denver']
    for city in cities:
        weather_data = pd.read_csv("csv/weather_data_"+city+".csv")
        air_quality_data = pd.read_csv("csv/aqi_cleaned_"+city+".csv")
        merged_data = joinFiles(air_quality_data, weather_data, city)
        merged_data['aqi_cat'] = merged_data['aqi'].apply(categorize_aqi)
        cat_dict = count_unique_values(merged_data, 'aqi_cat')
        print('city:', city, ' : ', cat_dict)
        merged_data.to_csv('csv/merged_data_'+city+'.csv', index=False)


