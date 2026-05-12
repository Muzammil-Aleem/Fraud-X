# import os
# import numpy as np
# import pandas as pd
# import joblib
# import warnings
# warnings.filterwarnings("ignore")

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.metrics import (
#     classification_report, confusion_matrix,
#     roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
# )
# from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier
# from imblearn.combine import SMOTETomek
# import shap

# import tensorflow as tf
# from tensorflow.keras.models import Sequential, Model
# from tensorflow.keras.layers import (
#     LSTM, Dense, Dropout, RepeatVector,
#     TimeDistributed, Input
# )
# from tensorflow.keras.callbacks import EarlyStopping

# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import seaborn as sns

# DATA_PATH   = "data/creditcard.csv"
# MODELS_DIR  = "models"
# PLOTS_DIR   = "plots"
# RANDOM_SEED = 42

# os.makedirs(MODELS_DIR, exist_ok=True)
# os.makedirs(PLOTS_DIR,  exist_ok=True)

# np.random.seed(RANDOM_SEED)
# tf.random.set_seed(RANDOM_SEED)

# def load_data(path: str):
#     df = pd.read_csv(path)
#     print(f"Shape: {df.shape}")
#     print(f"Fraud cases: {df['Class'].sum()} ({df['Class'].mean()*100:.3f}%)")
#     print(f"Legit cases: {(df['Class']==0).sum()}")
#     return df

# def base_preprocess(df: pd.DataFrame):
#     df = df.copy()
#     scaler = StandardScaler()
#     df["Amount_scaled"] = scaler.fit_transform(df[["Amount"]])
#     df["Time_scaled"]   = scaler.fit_transform(df[["Time"]])
#     df.drop(["Amount", "Time"], axis=1, inplace=True)
#     X = df.drop("Class", axis=1)
#     y = df["Class"]
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, stratify=y, random_state=RANDOM_SEED
#     )
#     return X_train, X_test, y_train, y_test, scaler

# def resample_probability_distribution(X_train, y_train, plot=True):
#     X_fraud = X_train[y_train == 1].values
#     X_legit = X_train[y_train == 0].values
#     mu_f,  std_f  = X_fraud.mean(axis=0), X_fraud.std(axis=0) + 1e-9
#     mu_l,  std_l  = X_legit.mean(axis=0), X_legit.std(axis=0) + 1e-9
#     def log_likelihood(X, mu, std):
#         return -0.5 * np.sum(((X - mu) / std) ** 2, axis=1)
#     ll_fraud_given_legit = log_likelihood(X_legit, mu_f, std_f)
#     ll_legit_given_legit = log_likelihood(X_legit, mu_l, std_l)
#     log_ratio = ll_fraud_given_legit - ll_legit_given_legit
#     fraud_prob_score = 1 / (1 + np.exp(-log_ratio))
#     n_fraud     = len(X_fraud)
#     n_keep_hard = min(n_fraud * 3, len(X_legit) // 2)
#     n_keep_rand = n_fraud * 3
#     hard_idx = np.argsort(fraud_prob_score)[::-1][:n_keep_hard]
#     rand_mask = np.ones(len(X_legit), dtype=bool)
#     rand_mask[hard_idx] = False
#     rand_idx  = np.random.choice(np.where(rand_mask)[0],
#                                  size=n_keep_rand, replace=False)
#     kept_idx  = np.union1d(hard_idx, rand_idx)
#     X_legit_kept = X_legit[kept_idx]
#     n_synth   = len(X_legit_kept) - n_fraud
#     synthetic = np.random.normal(loc=mu_f, scale=std_f, size=(n_synth, len(mu_f)))
#     for i in range(synthetic.shape[1]):
#         synthetic[:, i] = np.clip(synthetic[:, i],
#                                   X_fraud[:, i].min(),
#                                   X_fraud[:, i].max())
#     X_res = np.vstack([X_legit_kept, X_fraud, synthetic])
#     y_res = np.hstack([
#         np.zeros(len(X_legit_kept)),
#         np.ones(n_fraud),
#         np.ones(n_synth)
#     ])
#     perm  = np.random.permutation(len(X_res))
#     X_res, y_res = X_res[perm], y_res[perm]
#     return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)

# def resample_smote_tomek(X_train, y_train):
#     smt = SMOTETomek(random_state=RANDOM_SEED)
#     X_res, y_res = smt.fit_resample(X_train, y_train)
#     return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)

# def evaluate(name, y_test, y_pred, y_prob=None):
#     print(f"Results – {name}")
#     print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
#     print(f"Precision : {precision_score(y_test, y_pred, zero_division=0):.4f}")
#     print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
#     print(f"F1-Score  : {f1_score(y_test, y_pred):.4f}")
#     if y_prob is not None:
#         print(f"ROC-AUC   : {roc_auc_score(y_test, y_prob):.4f}")
#     print(classification_report(y_test, y_pred,
#                                  target_names=["Legit", "Fraud"],
#                                  zero_division=0))
#     return {
#         "accuracy":  accuracy_score(y_test, y_pred),
#         "precision": precision_score(y_test, y_pred, zero_division=0),
#         "recall":    recall_score(y_test, y_pred),
#         "f1":        f1_score(y_test, y_pred),
#         "roc_auc":   roc_auc_score(y_test, y_prob) if y_prob is not None else None,
#     }

# def path_a(X_train, X_test, y_train, y_test):
#     X_res, y_res = resample_probability_distribution(X_train, y_train, plot=True)
#     clf = XGBClassifier(
#         n_estimators=300,
#         max_depth=6,
#         learning_rate=0.05,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         scale_pos_weight=1,
#         use_label_encoder=False,
#         eval_metric="logloss",
#         random_state=RANDOM_SEED,
#         n_jobs=-1,
#     )
#     clf.fit(X_res, y_res,
#             eval_set=[(X_test, y_test)],
#             verbose=False)
#     y_pred = clf.predict(X_test)
#     y_prob = clf.predict_proba(X_test)[:, 1]
#     metrics_a = evaluate("PATH A – XGBoost + Prob-Distribution", y_test, y_pred, y_prob)
#     explainer  = shap.TreeExplainer(clf)
#     sample_idx = np.where(y_test.values == 1)[0][:50]
#     X_sample   = X_test.iloc[sample_idx]
#     shap_vals  = explainer.shap_values(X_sample)
#     joblib.dump(clf, f"{MODELS_DIR}/path_a_xgboost.pkl")
#     joblib.dump(X_train.columns.tolist(), f"{MODELS_DIR}/fraud_features.pkl")
#     return clf, metrics_a

# def build_lstm_autoencoder(timesteps: int, n_features: int) -> Model:
#     inp = Input(shape=(timesteps, n_features))
#     x   = LSTM(64, activation="tanh", return_sequences=False)(inp)
#     x   = Dropout(0.2)(x)
#     x   = Dense(16, activation="relu")(x)
#     x   = RepeatVector(timesteps)(x)
#     x   = LSTM(64, activation="tanh", return_sequences=True)(x)
#     x   = Dropout(0.2)(x)
#     out = TimeDistributed(Dense(n_features))(x)
#     model = Model(inputs=inp, outputs=out)
#     model.compile(optimizer="adam", loss="mse")
#     return model

# def path_b(X_train, X_test, y_train, y_test):
#     X_res, y_res = resample_smote_tomek(X_train, y_train)
#     X_legit_res = X_res[y_res == 0].values
#     TIMESTEPS   = 1
#     N_FEATURES  = X_legit_res.shape[1]
#     X_ae_train  = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
#     X_ae_test   = X_test.values.reshape(-1, TIMESTEPS, N_FEATURES)
#     autoencoder = build_lstm_autoencoder(TIMESTEPS, N_FEATURES)
#     autoencoder.fit(
#         X_ae_train, X_ae_train,
#         epochs=30,
#         batch_size=256,
#         validation_split=0.1,
#         callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
#         verbose=1,
#     )
#     X_train_3d   = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
#     recon_train  = autoencoder.predict(X_train_3d, verbose=0)
#     mse_train    = np.mean((X_train_3d - recon_train) ** 2, axis=(1, 2))
#     threshold    = np.percentile(mse_train, 95)
#     recon_test   = autoencoder.predict(X_ae_test, verbose=0)
#     mse_test     = np.mean((X_ae_test - recon_test) ** 2, axis=(1, 2))
#     y_pred       = (mse_test > threshold).astype(int)
#     metrics_b = evaluate("PATH B – LSTM Autoencoder", y_test, y_pred, mse_test)
#     autoencoder.save(f"{MODELS_DIR}/path_b_lstm_autoencoder.keras")
#     joblib.dump(threshold, f"{MODELS_DIR}/path_b_threshold.pkl")
#     return autoencoder, threshold, mse_test, metrics_b

# def path_c(X_train, X_test, y_train, y_test):
#     X_res, y_res = resample_smote_tomek(X_train, y_train)
#     xgb = XGBClassifier(
#         n_estimators=300, max_depth=6, learning_rate=0.05,
#         subsample=0.8, colsample_bytree=0.8,
#         use_label_encoder=False, eval_metric="logloss",
#         random_state=RANDOM_SEED, n_jobs=-1,
#     )
#     xgb.fit(X_res, y_res, verbose=False)
#     rf = RandomForestClassifier(
#         n_estimators=200, max_depth=None, min_samples_leaf=2,
#         class_weight="balanced", random_state=RANDOM_SEED, n_jobs=-1,
#     )
#     rf.fit(X_res, y_res)
#     prob_xgb   = xgb.predict_proba(X_test)[:, 1]
#     prob_rf    = rf.predict_proba(X_test)[:, 1]
#     prob_ens   = 0.6 * prob_xgb + 0.4 * prob_rf
#     thresholds = np.linspace(0.1, 0.9, 81)
#     f1s        = [f1_score(y_test, (prob_ens > t).astype(int), zero_division=0)
#                   for t in thresholds]
#     best_thresh = thresholds[np.argmax(f1s)]
#     y_pred     = (prob_ens > best_thresh).astype(int)
#     metrics_c  = evaluate("PATH C – Hybrid Ensemble", y_test, y_pred, prob_ens)
#     explainer  = shap.TreeExplainer(xgb)
#     sample_idx = np.where(y_test.values == 1)[0][:50]
#     X_sample   = X_test.iloc[sample_idx]
#     shap_vals  = explainer.shap_values(X_sample)
#     joblib.dump(xgb,         f"{MODELS_DIR}/path_c_xgb.pkl")
#     joblib.dump(rf,          f"{MODELS_DIR}/path_c_rf.pkl")
#     joblib.dump(best_thresh, f"{MODELS_DIR}/path_c_threshold.pkl")
#     return xgb, rf, best_thresh, metrics_c

# def print_comparison(metrics_a, metrics_b, metrics_c):
#     print("\n=== FraudX – Module 1: Path Comparison ===")
#     print("{:<25} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
#         "Path", "Accuracy", "Precision", "Recall", "F1", "ROC-AUC"))
#     for name, metrics in [
#         ("Path A (XGBoost+ProbDist)", metrics_a),
#         ("Path B (LSTM AutoEnc)", metrics_b),
#         ("Path C (Hybrid Ens)", metrics_c),
#     ]:
#         print("{:<25} {:<10.3f} {:<10.3f} {:<10.3f} {:<10.3f} {:<10.3f}".format(
#             name,
#             metrics.get("accuracy", 0),
#             metrics.get("precision", 0),
#             metrics.get("recall", 0),
#             metrics.get("f1", 0),
#             metrics.get("roc_auc", 0) if metrics.get("roc_auc") else 0,
#         ))

# def main():
#     df = load_data(DATA_PATH)
#     X_train, X_test, y_train, y_test, scaler = base_preprocess(df)
#     _, metrics_a = path_a(X_train, X_test, y_train, y_test)
#     _, _, _, metrics_b = path_b(X_train, X_test, y_train, y_test)
#     _, _, _, metrics_c = path_c(X_train, X_test, y_train, y_test)
#     print_comparison(metrics_a, metrics_b, metrics_c)
#     best = max(
#         [("Path A", metrics_a["f1"]),
#          ("Path B", metrics_b["f1"]),
#          ("Path C", metrics_c["f1"])],
#         key=lambda x: x[1]
#     )
#     print(f"WINNER: {best[0]}  (F1 = {best[1]:.4f})")

# if __name__ == "__main__":
#     main()


import os
import warnings
import numpy as np
import pandas as pd
import joblib

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from xgboost import XGBClassifier

DATA_PATH = "data/creditcard.csv"
MODELS_DIR = "models"

os.makedirs(MODELS_DIR, exist_ok=True)

RANDOM_SEED = 42

print("Loading Dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Dataset Shape : {df.shape}")
print(f"Fraud Cases   : {df['Class'].sum()}")
print(f"Legit Cases   : {(df['Class']==0).sum()}")

scaler = StandardScaler()

df["Amount_scaled"] = scaler.fit_transform(df[["Amount"]])
df["Time_scaled"] = scaler.fit_transform(df[["Time"]])

df.drop(["Amount", "Time"], axis=1, inplace=True)

X = df.drop("Class", axis=1)
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=RANDOM_SEED
)

print(f"\nTrain Samples : {len(X_train)}")
print(f"Test Samples  : {len(X_test)}")

print("\nApplying Probability Distribution Resampling...")

X_fraud = X_train[y_train == 1].values
X_legit = X_train[y_train == 0].values

mu_fraud = X_fraud.mean(axis=0)
std_fraud = X_fraud.std(axis=0) + 1e-9

mu_legit = X_legit.mean(axis=0)
std_legit = X_legit.std(axis=0) + 1e-9

def log_likelihood(X, mu, std):
    return -0.5 * np.sum(((X - mu) / std) ** 2, axis=1)

ll_fraud = log_likelihood(X_legit, mu_fraud, std_fraud)
ll_legit = log_likelihood(X_legit, mu_legit, std_legit)

log_ratio = ll_fraud - ll_legit

fraud_probability = 1 / (1 + np.exp(-log_ratio))

n_fraud = len(X_fraud)

hard_idx = np.argsort(fraud_probability)[::-1][:n_fraud * 3]

remaining_idx = np.setdiff1d(np.arange(len(X_legit)), hard_idx)

random_idx = np.random.choice(
    remaining_idx,
    size=n_fraud * 3,
    replace=False
)

selected_legit_idx = np.union1d(hard_idx, random_idx)

X_legit_selected = X_legit[selected_legit_idx]

n_synthetic = len(X_legit_selected) - n_fraud

synthetic_fraud = np.random.normal(
    loc=mu_fraud,
    scale=std_fraud,
    size=(n_synthetic, X_fraud.shape[1])
)

for i in range(synthetic_fraud.shape[1]):
    synthetic_fraud[:, i] = np.clip(
        synthetic_fraud[:, i],
        X_fraud[:, i].min(),
        X_fraud[:, i].max()
    )

X_resampled = np.vstack([
    X_legit_selected,
    X_fraud,
    synthetic_fraud
])

y_resampled = np.hstack([
    np.zeros(len(X_legit_selected)),
    np.ones(len(X_fraud)),
    np.ones(len(synthetic_fraud))
])

perm = np.random.permutation(len(X_resampled))

X_resampled = X_resampled[perm]
y_resampled = y_resampled[perm]

print(f"Resampled Dataset Size : {len(X_resampled)}")

X_resampled = pd.DataFrame(X_resampled, columns=X_train.columns)

print("\nTraining XGBoost Model...")

model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=RANDOM_SEED,
    n_jobs=-1
)

model.fit(X_resampled, y_resampled)

y_pred = model.predict(X_test)

y_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, zero_division=0)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print("XGBOOST + PROBABILITY DISTRIBUTION")

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
        target_names=["Legit", "Fraud"],
        zero_division=0
    )
)

joblib.dump(model, f"{MODELS_DIR}/fraud_xgboost_model.pkl")
joblib.dump(scaler, f"{MODELS_DIR}/fraud_scaler.pkl")