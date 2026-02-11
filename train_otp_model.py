import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

data = pd.read_csv("data/otp_dataset.csv")

X = data["text"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

joblib.dump(model, "models/otp_model.pkl")
joblib.dump(vectorizer, "models/otp_vectorizer.pkl")

print("OTP Scam Model Trained")
