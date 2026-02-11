import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("data/creditcard.csv")

# Features & label
X = data.drop("Class", axis=1)
y = data["Class"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier(n_estimators=50)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/fraud_model.pkl")

print("Fraud Model Trained & Saved")
