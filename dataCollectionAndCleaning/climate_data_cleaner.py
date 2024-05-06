import os
import pandas as pd


def arctic_cleaner():
    path = os.path.join(os.getcwd(), "data", "arctic_data.csv")
    df = pd.read_csv(path)

    df["day"] = 1

    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]], errors="coerce", format="%Y-%m-%d"
    )

    df = df.drop(
        columns=["Column1", "data-type", "hemisphere", "rank", "year", "month", "day"]
    )

    for column in df.columns:
        if column != "date":
            df["arctic_" + column] = df[column]
            df = df.drop(columns=[column])

    df.to_csv(path, index=False)


# arctic_cleaner()


def co2_cleaner():
    path = os.path.join(os.getcwd(), "data", "co2_data.csv")
    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]], errors="coerce", format="%Y-%m-%d"
    )

    df["co2_trend"] = df["trend"]
    df["co2_cycle"] = df["cycle"]

    df = df[["date", "co2_cycle", "co2_trend"]]

    df.to_csv(path, index=False)


# co2_cleaner()


def methane_cleaner():
    path = os.path.join(os.getcwd(), "data", "methane_data.csv")
    df = pd.read_csv(path)

    df[["year", "month"]] = df["date"].str.split(".", expand=True)
    df = df.drop(columns=["date"])
    df["day"] = 1

    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]], errors="coerce", format="%Y-%m-%d"
    )

    df = df.drop(columns=["year", "month", "day"])

    for column in df.columns:
        if column != "date":
            df["methane_" + column] = df[column]
            df = df.drop(columns=[column])

    df.to_csv(path, index=False)


# methane_cleaner()


def nitrous_cleaner():
    path = os.path.join(os.getcwd(), "data", "nitrous_data.csv")
    df = pd.read_csv(path)

    df["date"] = df["date"].astype(str)
    df[["year", "month"]] = df["date"].str.split(".", expand=True)
    df = df.drop(columns=["date"])
    df["day"] = 1

    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]], errors="coerce", format="%Y-%m-%d"
    )

    df = df.drop(columns=["year", "month", "day"])

    for column in df.columns:
        if column != "date":
            df["nitrous_" + column] = df[column]
            df = df.drop(columns=[column])

    df.to_csv(path, index=False)


# nitrous_cleaner()


def ocean_warming_cleaner():
    path = os.path.join(os.getcwd(), "data", "ocean_warming_data.csv")
    df = pd.read_csv(path)

    df["day"] = 1
    df["month"] = 1

    df["date"] = pd.to_datetime(
        df[["year", "month", "day"]], errors="coerce", format="%Y-%m-%d"
    )

    df = df.drop(columns=["year", "month", "day"])

    for column in df.columns:
        if column != "date":
            df["ocean_warming_" + column] = df[column]
            df = df.drop(columns=[column])

    df.to_csv(path, index=False)


# ocean_warming_cleaner()


def delete_before_1980():
    path = os.path.join(os.getcwd(), "data", "temperature_data.csv")
    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"])

    target_date = "1980-01-01"
    target_date = pd.to_datetime(target_date)

    df = df[df["date"] >= target_date]

    df.to_csv(path, index=False)


# delete_before_1980()


def temperature_cleaner():
    path = os.path.join(os.getcwd(), "data", "temperature_data.csv")
    df = pd.read_csv(path)

    def convert_fractional_year_to_datetime(year):
        year_int = int(year)
        remainder = year - year_int
        base = pd.Timestamp(str(year_int))
        result = base + pd.Timedelta(seconds=(remainder * 365.25 * 24 * 60 * 60))
        return result.strftime("%Y-%m-%d")  # Formatting to 'yyyy-mm-dd'

    df["date"] = df["time"].apply(convert_fractional_year_to_datetime)

    df = df.drop(columns=["time"])

    for column in df.columns:
        if column != "date":
            df["temperature_" + column] = df[column]
            df = df.drop(columns=[column])

    df.to_csv(path, index=False)


# temperature_cleaner()


def delete_duplicates():
    path = os.path.join(os.getcwd(), "data", "methane_data.csv")
    df = pd.read_csv(path)
    date_column = "date"
    if date_column not in df.columns:
        print(f"The specified column '{date_column}' does not exist in the DataFrame.")
        return df

    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")

    df = df.dropna(subset=[date_column])

    df = df.drop_duplicates(subset=[date_column], keep="first")
    df.to_csv(path, index=False)


# delete_duplicates()


def combine_csvs():
    path_to_csvs = os.path.join(os.getcwd(), "data")
    dfs = []

    for filename in os.listdir(path_to_csvs):
        if filename.endswith(".csv"):
            file_path = os.path.join(path_to_csvs, filename)
            df = pd.read_csv(file_path)
            df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
            if df["date"].is_unique:
                df.set_index("date", inplace=True)
                dfs.append(df)
            else:
                print(
                    f"Duplicate dates found in {filename}. Consider reviewing the data."
                )

    combined_df = pd.concat(dfs, axis=1)
    combined_df.reset_index(inplace=True)
    print(combined_df.head())
    combined_df.to_csv(os.path.join(path_to_csvs, "combined_data.csv"), index=False)


# combine_csvs()
import json
from datetime import datetime, timedelta


def land_surface_temp_cleaner():
    df = pd.DataFrame(columns=["date", "value"])
    path = os.path.join(
        os.getcwd(), "data", "climate_change_data", "sea_surface_temperature.json"
    )
    data_rows = []
    with open(path, "r") as f:
        json_data = json.load(f)

    for item in json_data:
        year = int(item["name"])
        data = item["data"]
        start_date = datetime(year, 1, 1)

        for i, value in enumerate(data):
            date = start_date + timedelta(days=i)
            data_rows.append({'date': date.strftime('%Y/%m/%d'), 'sea_surface_temp(C)': value})

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data_rows)
    df.to_csv(
        os.path.join(
            os.getcwd(), "data", "climate_change_data", "sea_surface_temperature.csv"
        ),
        index=False,
    )

    print(df.head())


# land_surface_temp_cleaner()


def sea_ice_cleaner():
    path = os.path.join(
        os.getcwd(), "data", "climate_change_data", "sea_ice_extent.csv"
    )
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')

    df = df.drop(columns=['Year', 'Month', 'Day', 'Missing(10^6 sq km)', 'Source Data'])
    df = df[["Date", "Extent(10^6 sq km)"]]
    df.to_csv(os.path.join(
        os.getcwd(), "data", "climate_change_data", "sea_ice_extent1.csv"
    ), index=False)

# sea_ice_cleaner()
    
def climate_change_combine():
    path_to_csvs = os.path.join(os.getcwd(), "data", "climate_change_data")
    dfs = []

    for filename in os.listdir(path_to_csvs):
        if filename.endswith(".csv"):
            file_path = os.path.join(path_to_csvs, filename)
            df = pd.read_csv(file_path)
            df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d")
            if df["Date"].is_unique:
                df.set_index("Date", inplace=True)
                dfs.append(df)
            else:
                print(
                    f"Duplicate dates found in {filename}. Consider reviewing the data."
                )

    combined_df = pd.concat(dfs, axis=1)
    combined_df.reset_index(inplace=True)
    print(combined_df.head())
    combined_df.to_csv(os.path.join(path_to_csvs, "combined_climate_change_data.csv"), index=False)


# climate_change_combine()
    
