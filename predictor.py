import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score

matches = pd.read_csv("matches.csv", index_col=0)
matches["Date"] = pd.to_datetime(matches["Date"])  # converts date column from object to datetime.
matches["oppCode"] = matches["Opponent"].astype("category").cat.codes  # adds a column to keep track of opponents using a code.
matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype(int)  # adds a column to keep the Hour time simpler.
matches["dayCode"] = matches["Date"].dt.dayofweek  # adds a column to keep track of days using a code.
matches["Target"] = (matches["Result"] == "W").astype(int)  # adds a column to keep track of result using a code.

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

# Create combined DataFrame
combined = pd.DataFrame({"actual": test_y.values, "prediction": predict})

# Print confusion matrix
confusion_matrix = pd.crosstab(index=combined["actual"], columns=combined["prediction"], rownames=['Actual'], colnames=['Predicted'])
precision = precision_score(test_y, predict)
print(precision)