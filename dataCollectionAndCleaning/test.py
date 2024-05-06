import os
import pandas as pd

path = os.path.join(os.getcwd(), "data", "AQI.csv")
print(path)

df = pd.read_csv(path)
print(df)
df.info()