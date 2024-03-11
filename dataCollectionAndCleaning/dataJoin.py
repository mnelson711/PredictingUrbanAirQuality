#This file will join the AQI and Weather Data by time to create one mega, super awesome, computer crashing csv file
import pandas as pd

def joinFiles(air_quality_data, weather_data):
    #initial cleanup
    weather_data = weather_data.dropna(subset=['time','year', 'month', 'day'])
    air_quality_data = air_quality_data.dropna(subset=['time','year', 'month', 'day'])
    weather_data['time'] = weather_data['time'].str.slice(0, 5)
    
    merged_data = pd.merge(weather_data, air_quality_data, on=['time','day', 'month', 'year'], how='inner')
    #final cleanup
    merged_data.drop_duplicates(inplace=True)
    merged_data.drop(columns=['lat', 'lon','dt'], inplace=True)
    merged_data.to_csv("csv/merged_data.csv", index=False)
    print('finished merging')
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

import matplotlib.pyplot as plt

def plot_category_counts(count_dict, title='Category Counts', xlabel='Category', ylabel='Count'):
    """
    Plots a bar graph of category counts.

    Parameters:
    - count_dict: dict, a dictionary with categories as keys and counts as values.
    - title: str, the title of the plot.
    - xlabel: str, the label for the x-axis.
    - ylabel: str, the label for the y-axis.
    """
    # Categories and their counts
    categories = list(count_dict.keys())
    counts = list(count_dict.values())
    
    # Creating the bar plot
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
    plt.bar(categories, counts, color='skyblue')  # You can change the color
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.xticks(rotation=45)  # Rotates the category names to avoid overlap
    plt.show()
    
def plot_category_counts_log_scale(count_dict, title='Category Counts', xlabel='Category', ylabel='Count', log_scale=True):
    """
    Plots a bar graph of category counts with an option for a logarithmic scale.

    Parameters:
    - count_dict: dict, a dictionary with categories as keys and counts as values.
    - title: str, the title of the plot.
    - xlabel: str, the label for the x-axis.
    - ylabel: str, the label for the y-axis.
    - log_scale: bool, whether to use a logarithmic scale for the y-axis.
    """
    categories = list(count_dict.keys())
    counts = list(count_dict.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts, color='skyblue')
    
    if log_scale:
        plt.yscale('log')  # Apply logarithmic scale
        plt.ylabel(ylabel + ' (log scale)')
    else:
        plt.ylabel(ylabel)
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45)
    
    # Adding a minimum value for y-axis when log scale is used to avoid log(0)
    if log_scale:
        plt.ylim(bottom=max(min(counts), 0.1))  # Sets the bottom to the smallest non-zero count or 0.1
    
    plt.show()

if __name__ == "__main__":
    # weather_data = pd.read_csv("csv/weather_data_Boston_processed.csv", nrows=1000000)
    # air_quality_data = pd.read_csv("csv/aqi_cleaned_Boston.csv", nrows=1000000)
    # merged_data = joinFiles(air_quality_data, weather_data)
    # Applying the function to create a new column
    merged_data = pd.read_csv("../csv/merged_data.csv", low_memory=False)
    merged_data['aqi_cat'] = merged_data['aqi'].apply(categorize_aqi)
    cat_dict = count_unique_values(merged_data, 'aqi_cat')
    plot_category_counts_log_scale(cat_dict, title='Category Counts', xlabel='Category', ylabel='Count', log_scale=True)    # print(merged_data['aqi_cat'])
    merged_data.to_csv('../csv/merged_data.csv', index=False)


