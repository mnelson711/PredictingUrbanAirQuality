import os
import pandas as pd
import numpy as np


def split_csv():
    path = os.path.join(os.getcwd(), "data", "AQI.csv")
    df = pd.read_csv(path)
    midpoint_index = len(df) // 2

    first_half = df.iloc[:midpoint_index]
    second_half = df.iloc[midpoint_index:]

    first_half.to_csv(
        os.path.join(os.getcwd(), "data", "first_half_AQI.csv"), index=False
    )

    second_half.to_csv(
        os.path.join(os.getcwd(), "data", "second_half_AQI.csv"), index=False
    )


# split_csv()


def combine_csv():
    first_half = pd.read_csv(os.path.join(os.getcwd(), "data", "first_half_AQI.csv"))
    second_half = pd.read_csv(os.path.join(os.getcwd(), "data", "second_half_AQI.csv"))

    combined = pd.concat([first_half, second_half])
    combined.to_csv(os.path.join(os.getcwd(), "data", "combined_AQI.csv"), index=False)


# combine_csv()


def info():
    path = os.path.join(os.getcwd(), "data", "climate_change_AQI.csv")
    df = pd.read_csv(path)
    print(df.info())
    print(df.head())
    print(df.describe())
    length = int(len(df))
    for i in range(0, length, int(length / 10)):
        print(df.iloc[i])


# info()


def combine_rows():
    path = os.path.join(os.getcwd(), "data", "AQI.csv")
    df = pd.read_csv(path)
    df["Longitude"] = df["Longitude"].astype(float)
    df["Latitude"] = df["Latitude"].astype(float)
    df["Date Local"] = pd.to_datetime(df["Date Local"])

    # Aggregate the data
    df_aggregated = (
        df.groupby(["Longitude", "Latitude", "Date Local"])
        .agg(
            {
                "Ozone": "max",
                "Sulfer Dioxide": "max",
                "Nitrogen Dioxide": "max",
                "Carbon Monoxide": "max",
            }
        )
        .reset_index()
    )
    df_aggregated.to_csv(
        os.path.join(os.getcwd(), "data", "AQI_combined.csv"), index=False
    )


# combine_rows()


def just_Ozone():
    path = os.path.join(os.getcwd(), "data", "AQI_combined.csv")
    df = pd.read_csv(path)
    df["Longitude"] = df["Longitude"].astype(float)
    df["Latitude"] = df["Latitude"].astype(float)
    df["Date Local"] = pd.to_datetime(df["Date Local"])

    df_aggregated = (
        df.groupby(["Longitude", "Latitude", "Date Local"])
        .agg({"Ozone": "max"})
        .reset_index()
    )
    df_aggregated.to_csv(
        os.path.join(os.getcwd(), "data", "AQI_Ozone.csv"), index=False
    )


# just_Ozone()


def location_count():
    path = os.path.join(os.getcwd(), "data", "AQI_combined.csv")
    df = pd.read_csv(path)
    print(df["Longitude"].value_counts())
    print(df["Latitude"].value_counts())


# location_count()


def only_top_10_locations():
    path = os.path.join(os.getcwd(), "data", "AQI_combined.csv")
    df = pd.read_csv(path)
    longitude_counts = df["Longitude"].value_counts()
    latitude_counts = df["Latitude"].value_counts()

    top_10_longitudes = longitude_counts.head(10).index
    top_10_latitudes = latitude_counts.head(10).index

    df = df[
        df["Longitude"].isin(top_10_longitudes) & df["Latitude"].isin(top_10_latitudes)
    ]
    df.to_csv(os.path.join(os.getcwd(), "data", "AQI_top_10.csv"), index=False)


# only_top_10_locations()


def add_cyclical_time():
    path = os.path.join(os.getcwd(), "data", "AQI_combined.csv")
    df = pd.read_csv(path)
    df["Date Local"] = pd.to_datetime(df["Date Local"])

    df["Day of Year"] = df["Date Local"].dt.dayofyear

    df["Days in Year"] = df["Date Local"].dt.is_leap_year.map({True: 366, False: 365})

    df["Sine"] = np.sin(2 * np.pi * df["Day of Year"] / df["Days in Year"])
    df["Cosine"] = np.cos(2 * np.pi * df["Day of Year"] / df["Days in Year"])

    df.drop(columns=["Day of Year", "Days in Year"], inplace=True)
    df.to_csv(os.path.join(os.getcwd(), "data", "AQI_cyclical.csv"), index=False)


# add_cyclical_time()


def combine_AQI_climate_change():
    AQI_path = os.path.join(os.getcwd(), "data", "AQI_cyclical.csv")
    Climate_path = os.path.join(
        os.getcwd(), "data", "climate_change_data", "combined_climate_change_data.csv"
    )
    AQI_df = pd.read_csv(AQI_path)
    Climate_df = pd.read_csv(Climate_path)
    AQI_df["Date"] = AQI_df["Date Local"]
    AQI_df.drop(
        columns=["Date Local", "Sulfer Dioxide", "Nitrogen Dioxide", "Carbon Monoxide"],
        inplace=True,
    )
    merged_df = pd.merge(AQI_df, Climate_df, on="Date", how="inner")
    merged_df.dropna(inplace=True)
    merged_df.to_csv(
        os.path.join(os.getcwd(), "data", "climate_change_AQI.csv"), index=False
    )


# combine_AQI_climate_change()
