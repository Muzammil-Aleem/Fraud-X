import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

from sklearn.model_selection import train_test_split

data = pd.read_csv("data/otp_dataset.csv")

data.dropna(inplace=True)

data["label"] = data["label"].map({
    "fake": 0,
    "real": 1
})

X = data["text"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    ngram_range=(1, 3),
    max_features=10000,
    min_df=1
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)

joblib.dump(model, "models/otp_model.pkl")
joblib.dump(vectorizer, "models/otp_vectorizer.pkl")

print("OTP Scam Model Trained Successfully")

y_pred = model.predict(X_test_vec)

y_prob = model.predict_proba(X_test_vec)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred, zero_division=0)
f1 = f1_score(y_test, y_pred, zero_division=0)
roc_auc = roc_auc_score(y_test, y_prob)

print("MODEL EVALUATION")

print(f"Accuracy Score : {accuracy:.4f}")
print(f"Precision Score: {precision:.4f}")
print(f"Recall Score   : {recall:.4f}")
print(f"F1 Score       : {f1:.4f}")
print(f"ROC-AUC Score  : {roc_auc:.4f}")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["fake", "real"],
        zero_division=0
    )
)