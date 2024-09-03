import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score

# Read and preprocess the data
matches = pd.read_csv("matches.csv", index_col=0)
matches["Date"] = pd.to_datetime(matches["Date"])
matches["oppCode"] = matches["Opponent"].astype("category").cat.codes
matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype(int)
matches["dayCode"] = matches["Date"].dt.dayofweek
matches["Target"] = (matches["Result"] == "W").astype(int)

# Map opponents to standardized names
mapValues = {
    "it Italy": "Italy",
    "hr Croatia": "Croatia",
    "es Spain": "Spain",
    "fr France": "France",
    "pl Poland": "Poland",
    "nl Netherlands": "Netherlands",
    "tr Türkiye": "Turkiye",
    "sk Slovakia": "Slovakia",
    "ro Romania": "Romania",
    "ua Ukraine": "Ukraine",
    "al Albania": "Albania",
    "pt Portugal": "Portugal",
    "ge Georgia": "Georgia",
    "si Slovenia": "Slovenia",
    "eng England": "England",
    "rs Serbia": "Serbia",
    "de Germany": "Germany",
    "dk Denmark": "Denmark",
    "ch Switzerland": "Switzerland",
    "at Austria": "Austria",
    "be Belgium": "Belgium",
    "cz Czechia": "Czechia",
    "sct Scotland": "Scotland",
    "hu Hungary": "Hungary"
}

# Create a mapping dictionary
mapping = pd.Series(mapValues).to_dict()
matches["StandardizedOpponent"] = matches["Opponent"].map(mapping)

# Define predictors and target
predictors = ["oppCode", "Hour", "dayCode"]
X = matches[predictors]
y = matches["Target"]
split_index = int(len(matches) * 0.7)  # 70% for training, 30% for testing

# Train/test split
train_X = X[:split_index]
train_y = y[:split_index]
test_X = X[split_index:]
test_y = y[split_index:]

# Train the model
rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
rf.fit(train_X, train_y)

# Predict and evaluate accuracy
predict = rf.predict(test_X)
acc = accuracy_score(test_y, predict)
precision = precision_score(test_y, predict)
print(f"Accuracy Score: {acc}")
print(f"Precision Score: {precision}")

# Create combined DataFrame for predictions
test_matches = matches.iloc[split_index:].copy()
test_matches["actual"] = test_y.values
test_matches["prediction"] = predict

print("Combined DataFrame with predictions:")
print(test_matches.head(15))
test_matches.to_csv("predictions.csv")


# Check counts of actual vs predicted results
confusion_matrix = pd.crosstab(test_matches["actual"], test_matches["prediction"], rownames=['Actual'], colnames=['Predicted'])
print(confusion_matrix)
