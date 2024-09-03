import pandas as pd

matches = pd.read_csv("matches.csv", index_col=0)
matches["Date"] = pd.to_datetime(matches["Date"])  # converts date column from object to datetime.
matches["oppCode"] = matches["Opponent"].astype("category").cat.codes  # adds a column to keep track of opponents using a code.
matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype(int)  # adds a column to keep the Hour time simpler.
matches["dayCode"] = matches["Date"].dt.dayofweek  # adds a column to keep track of days using a code.
matches["Target"] = (matches["Result"] == "W").astype(int)  # adds a column to keep track of result using a code.
