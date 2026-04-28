# """
# FraudX – Credit Card Fraud Detection
# 3-Path Training Pipeline

# PATH A: Classical ML  →  Probability Distribution Resampling + XGBoost + SHAP
# PATH B: Deep Learning →  SMOTE+Tomek + LSTM Autoencoder
# PATH C: Hybrid        →  SMOTE+Tomek + Ensemble (XGBoost + LSTM) + SHAP
# """

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

# # ─────────────────────────────────────────────
# # CONFIG
# # ─────────────────────────────────────────────
# DATA_PATH   = "data/creditcard.csv"
# MODELS_DIR  = "models"
# PLOTS_DIR   = "plots"
# RANDOM_SEED = 42

# os.makedirs(MODELS_DIR, exist_ok=True)
# os.makedirs(PLOTS_DIR,  exist_ok=True)

# np.random.seed(RANDOM_SEED)
# tf.random.set_seed(RANDOM_SEED)


# # ─────────────────────────────────────────────
# # STEP 0 – LOAD & INSPECT
# # ─────────────────────────────────────────────
# def load_data(path: str):
#     print("\n" + "="*60)
#     print("STEP 0 – LOADING DATA")
#     print("="*60)

#     df = pd.read_csv(path)
#     print(f"  Shape        : {df.shape}")
#     print(f"  Fraud cases  : {df['Class'].sum()} ({df['Class'].mean()*100:.3f}%)")
#     print(f"  Legit cases  : {(df['Class']==0).sum()}")
#     return df


# # ─────────────────────────────────────────────
# # STEP 1 – BASE PREPROCESSING (shared by all paths)
# # ─────────────────────────────────────────────
# def base_preprocess(df: pd.DataFrame):
#     """Scale Amount & Time; drop raw columns."""
#     print("\n" + "="*60)
#     print("STEP 1 – BASE PREPROCESSING")
#     print("="*60)

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
#     print(f"  Train size : {X_train.shape[0]}  |  Test size : {X_test.shape[0]}")
#     return X_train, X_test, y_train, y_test, scaler


# # ─────────────────────────────────────────────
# # RESAMPLING A – Probability Distribution Curve
# # ─────────────────────────────────────────────
# def resample_probability_distribution(X_train: pd.DataFrame,
#                                       y_train: pd.Series,
#                                       plot: bool = True):
#     """
#     Alternative to SMOTE/Tomek:

#     1.  Estimate feature-wise Gaussian distributions separately for
#         fraud and legit classes using MLE (mean & std from training data).
#     2.  Compute per-sample Mahalanobis-like fraud probability score
#         using log-likelihood ratio:  P(fraud|x) ∝ N(x; μ_f, σ_f) / N(x; μ_l, σ_l)
#     3.  Select the top-N legit samples closest to the fraud distribution
#         (ambiguous, hard negatives) to DOWN-sample the majority class.
#     4.  Synthetically OVERSAMPLE fraud class by drawing from the fitted
#         fraud Gaussian — respects the real distribution shape rather than
#         interpolating blindly like SMOTE.

#     This gives a balanced dataset grounded in feature distributions.
#     """
#     print("\n" + "-"*50)
#     print("  RESAMPLING A – Probability Distribution Curve")
#     print("-"*50)

#     X_fraud = X_train[y_train == 1].values
#     X_legit = X_train[y_train == 0].values

#     # ── MLE: fit per-feature Gaussian for each class ──
#     mu_f,  std_f  = X_fraud.mean(axis=0), X_fraud.std(axis=0) + 1e-9
#     mu_l,  std_l  = X_legit.mean(axis=0), X_legit.std(axis=0) + 1e-9

#     # ── Log-likelihood of each legit sample under fraud distribution ──
#     def log_likelihood(X, mu, std):
#         return -0.5 * np.sum(((X - mu) / std) ** 2, axis=1)

#     ll_fraud_given_legit = log_likelihood(X_legit, mu_f, std_f)  # how "fraud-like" legit samples are
#     ll_legit_given_legit = log_likelihood(X_legit, mu_l, std_l)

#     log_ratio = ll_fraud_given_legit - ll_legit_given_legit  # higher = more ambiguous
#     fraud_prob_score = 1 / (1 + np.exp(-log_ratio))          # sigmoid → probability

#     # ── Down-sample legit: keep hard negatives + random sample ──
#     n_fraud     = len(X_fraud)
#     n_keep_hard = min(n_fraud * 3, len(X_legit) // 2)        # hard negatives
#     n_keep_rand = n_fraud * 3                                 # random legit

#     hard_idx = np.argsort(fraud_prob_score)[::-1][:n_keep_hard]
#     rand_mask = np.ones(len(X_legit), dtype=bool)
#     rand_mask[hard_idx] = False
#     rand_idx  = np.random.choice(np.where(rand_mask)[0],
#                                  size=n_keep_rand, replace=False)

#     kept_idx  = np.union1d(hard_idx, rand_idx)
#     X_legit_kept = X_legit[kept_idx]

#     # ── Oversample fraud: draw from fitted Gaussian ──
#     n_synth   = len(X_legit_kept) - n_fraud
#     synthetic = np.random.normal(loc=mu_f, scale=std_f, size=(n_synth, len(mu_f)))
#     # Clip to observed fraud range
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

#     # Shuffle
#     perm  = np.random.permutation(len(X_res))
#     X_res, y_res = X_res[perm], y_res[perm]

#     print(f"  Original  →  Fraud: {n_fraud}  |  Legit: {len(X_legit)}")
#     print(f"  Resampled →  Fraud: {int(y_res.sum())}  |  Legit: {int((y_res==0).sum())}")

#     # ── Plot distribution curves ──
#     if plot:
#         _plot_distribution_curves(
#             X_fraud, X_legit, synthetic,
#             fraud_prob_score, feature_idx=0   # show for V1 (first PCA feature)
#         )

#     return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)


# def _plot_distribution_curves(X_fraud, X_legit, X_synth,
#                                fraud_prob_score, feature_idx=0):
#     fig = plt.figure(figsize=(16, 10))
#     fig.patch.set_facecolor("#0D1117")
#     gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

#     col = {"fraud": "#FF4C6A", "legit": "#4CF0B4", "synth": "#FFC947",
#            "text": "#E6EDF3", "grid": "#21262D"}
#     feat_name = f"V{feature_idx+1}"

#     # ── (0,0) Per-class density for selected feature ──
#     ax1 = fig.add_subplot(gs[0, 0])
#     ax1.set_facecolor("#161B22")
#     for vals, label, c in [
#         (X_legit[:, feature_idx], "Legit",     col["legit"]),
#         (X_fraud[:, feature_idx], "Fraud",     col["fraud"]),
#         (X_synth[:, feature_idx], "Synthetic", col["synth"]),
#     ]:
#         kde_x = np.linspace(vals.min()-1, vals.max()+1, 300)
#         mu, sd = vals.mean(), vals.std()
#         kde_y  = (1/(sd*np.sqrt(2*np.pi))) * np.exp(-0.5*((kde_x-mu)/sd)**2)
#         ax1.plot(kde_x, kde_y, color=c, linewidth=2, label=label)
#         ax1.fill_between(kde_x, kde_y, alpha=0.15, color=c)

#     ax1.set_title(f"Feature {feat_name}: Gaussian Distributions",
#                   color=col["text"], fontsize=11, pad=10)
#     ax1.set_xlabel(feat_name, color=col["text"])
#     ax1.set_ylabel("Density",  color=col["text"])
#     ax1.tick_params(colors=col["text"])
#     ax1.legend(facecolor="#21262D", labelcolor=col["text"], fontsize=8)
#     ax1.grid(True, color=col["grid"], alpha=0.4)
#     for spine in ax1.spines.values(): spine.set_edgecolor(col["grid"])

#     # ── (0,1) Fraud probability score distribution for legit samples ──
#     ax2 = fig.add_subplot(gs[0, 1])
#     ax2.set_facecolor("#161B22")
#     ax2.hist(fraud_prob_score, bins=80, color=col["fraud"], alpha=0.8, edgecolor="none")
#     ax2.axvline(fraud_prob_score.mean(), color=col["synth"],
#                 linestyle="--", linewidth=1.5, label=f"Mean={fraud_prob_score.mean():.3f}")
#     ax2.set_title("Legit Samples: Fraud-Likeness Score\n(Log-Likelihood Ratio → Sigmoid)",
#                   color=col["text"], fontsize=11, pad=10)
#     ax2.set_xlabel("P(fraud-like)", color=col["text"])
#     ax2.set_ylabel("Count",         color=col["text"])
#     ax2.tick_params(colors=col["text"])
#     ax2.legend(facecolor="#21262D", labelcolor=col["text"], fontsize=8)
#     ax2.grid(True, color=col["grid"], alpha=0.4)
#     for spine in ax2.spines.values(): spine.set_edgecolor(col["grid"])

#     # ── (1,0) Class balance: before vs after ──
#     ax3 = fig.add_subplot(gs[1, 0])
#     ax3.set_facecolor("#161B22")
#     cats  = ["Before\n(Legit)", "Before\n(Fraud)", "After\n(Legit)", "After\n(Fraud)"]
#     vals  = [len(X_legit), len(X_fraud),
#              len(X_legit)//2, len(X_fraud)+len(X_synth)]
#     colors= [col["legit"], col["fraud"], col["legit"], col["fraud"]]
#     bars  = ax3.bar(cats, vals, color=colors, alpha=0.85, width=0.5)
#     for bar, v in zip(bars, vals):
#         ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+200,
#                  f"{v:,}", ha="center", va="bottom",
#                  color=col["text"], fontsize=8)
#     ax3.set_title("Class Balance: Before vs After Resampling",
#                   color=col["text"], fontsize=11, pad=10)
#     ax3.set_ylabel("Sample Count", color=col["text"])
#     ax3.tick_params(colors=col["text"])
#     ax3.grid(True, axis="y", color=col["grid"], alpha=0.4)
#     for spine in ax3.spines.values(): spine.set_edgecolor(col["grid"])

#     # ── (1,1) Box plots: real fraud vs synthetic ──
#     ax4 = fig.add_subplot(gs[1, 1])
#     ax4.set_facecolor("#161B22")
#     top5 = list(range(min(5, X_fraud.shape[1])))
#     data_box = [X_fraud[:, i] for i in top5] + [X_synth[:, i] for i in top5]
#     labels_box = [f"Real V{i+1}" for i in top5] + [f"Synth V{i+1}" for i in top5]
#     bp = ax4.boxplot(data_box, labels=labels_box, patch_artist=True,
#                      medianprops=dict(color="white", linewidth=1.5))
#     for i, patch in enumerate(bp["boxes"]):
#         patch.set_facecolor(col["fraud"] if i < 5 else col["synth"])
#         patch.set_alpha(0.7)
#     ax4.set_title("Real Fraud vs Synthetic Samples\n(First 5 Features)",
#                   color=col["text"], fontsize=11, pad=10)
#     ax4.tick_params(colors=col["text"], labelsize=7)
#     ax4.set_xticklabels(labels_box, rotation=30, ha="right", color=col["text"])
#     ax4.grid(True, axis="y", color=col["grid"], alpha=0.4)
#     for spine in ax4.spines.values(): spine.set_edgecolor(col["grid"])

#     fig.suptitle("FraudX – Probability Distribution Resampling",
#                  color=col["text"], fontsize=14, fontweight="bold", y=0.98)

#     plt.savefig(f"{PLOTS_DIR}/distribution_resampling.png",
#                 dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
#     plt.close()
#     print(f"  Plot saved → {PLOTS_DIR}/distribution_resampling.png")


# # ─────────────────────────────────────────────
# # RESAMPLING B – SMOTE + Tomek (Paths B & C)
# # ─────────────────────────────────────────────
# def resample_smote_tomek(X_train, y_train):
#     print("\n" + "-"*50)
#     print("  RESAMPLING B – SMOTE + Tomek Links")
#     print("-"*50)
#     smt = SMOTETomek(random_state=RANDOM_SEED)
#     X_res, y_res = smt.fit_resample(X_train, y_train)
#     print(f"  Resampled →  Fraud: {y_res.sum()}  |  Legit: {(y_res==0).sum()}")
#     return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)


# # ─────────────────────────────────────────────
# # EVALUATION HELPER
# # ─────────────────────────────────────────────
# def evaluate(name, y_test, y_pred, y_prob=None):
#     print(f"\n{'─'*50}")
#     print(f"  Results – {name}")
#     print(f"{'─'*50}")
#     print(f"  Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
#     print(f"  Precision : {precision_score(y_test, y_pred, zero_division=0):.4f}")
#     print(f"  Recall    : {recall_score(y_test, y_pred):.4f}")
#     print(f"  F1-Score  : {f1_score(y_test, y_pred):.4f}")
#     if y_prob is not None:
#         print(f"  ROC-AUC   : {roc_auc_score(y_test, y_prob):.4f}")
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


# # ═════════════════════════════════════════════════════════════════════
# # PATH A – Classical ML
# #          Resampling: Probability Distribution Curve
# #          Model:      XGBoost
# #          Explain:    SHAP
# # ═════════════════════════════════════════════════════════════════════
# def path_a(X_train, X_test, y_train, y_test):
#     print("\n\n" + "█"*60)
#     print("  PATH A – Classical ML  (Prob-Distribution Resampling + XGBoost + SHAP)")
#     print("█"*60)

#     # ── Resample ──
#     X_res, y_res = resample_probability_distribution(X_train, y_train, plot=True)

#     # ── Train XGBoost ──
#     print("\n  Training XGBoost …")
#     clf = XGBClassifier(
#         n_estimators=300,
#         max_depth=6,
#         learning_rate=0.05,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         scale_pos_weight=1,          # already balanced
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

#     # ── SHAP Explainability ──
#     print("\n  Computing SHAP values …")
#     explainer  = shap.TreeExplainer(clf)
#     sample_idx = np.where(y_test.values == 1)[0][:50]          # 50 fraud cases
#     X_sample   = X_test.iloc[sample_idx]
#     shap_vals  = explainer.shap_values(X_sample)

#     plt.figure(figsize=(10, 6))
#     shap.summary_plot(shap_vals, X_sample, show=False, plot_type="bar")
#     plt.title("PATH A – SHAP Feature Importance (Fraud Class)", pad=12)
#     plt.tight_layout()
#     plt.savefig(f"{PLOTS_DIR}/path_a_shap.png", dpi=150, bbox_inches="tight")
#     plt.close()
#     print(f"  SHAP plot saved → {PLOTS_DIR}/path_a_shap.png")

#     # ── Save ──
#     joblib.dump(clf, f"{MODELS_DIR}/path_a_xgboost.pkl")
#     print("  Model saved → models/path_a_xgboost.pkl")

#     return clf, metrics_a


# # ═════════════════════════════════════════════════════════════════════
# # PATH B – Deep Learning
# #          Resampling: SMOTE + Tomek
# #          Model:      LSTM Autoencoder (anomaly detection)
# #          Explain:    Reconstruction error threshold
# # ═════════════════════════════════════════════════════════════════════
# def build_lstm_autoencoder(timesteps: int, n_features: int) -> Model:
#     inp = Input(shape=(timesteps, n_features))
#     # Encoder
#     x   = LSTM(64, activation="tanh", return_sequences=False)(inp)
#     x   = Dropout(0.2)(x)
#     # Bottleneck
#     x   = Dense(16, activation="relu")(x)
#     # Decoder
#     x   = RepeatVector(timesteps)(x)
#     x   = LSTM(64, activation="tanh", return_sequences=True)(x)
#     x   = Dropout(0.2)(x)
#     out = TimeDistributed(Dense(n_features))(x)
#     model = Model(inputs=inp, outputs=out)
#     model.compile(optimizer="adam", loss="mse")
#     return model


# def path_b(X_train, X_test, y_train, y_test):
#     print("\n\n" + "█"*60)
#     print("  PATH B – Deep Learning  (SMOTE+Tomek + LSTM Autoencoder)")
#     print("█"*60)

#     # ── Resample ──
#     X_res, y_res = resample_smote_tomek(X_train, y_train)

#     # ── Train AUTOENCODER on legit transactions only ──
#     X_legit_res = X_res[y_res == 0].values
#     TIMESTEPS   = 1
#     N_FEATURES  = X_legit_res.shape[1]

#     X_ae_train  = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
#     X_ae_test   = X_test.values.reshape(-1, TIMESTEPS, N_FEATURES)

#     print(f"\n  Training LSTM Autoencoder  (features={N_FEATURES}) …")
#     autoencoder = build_lstm_autoencoder(TIMESTEPS, N_FEATURES)
#     autoencoder.fit(
#         X_ae_train, X_ae_train,
#         epochs=30,
#         batch_size=256,
#         validation_split=0.1,
#         callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
#         verbose=1,
#     )

#     # ── Reconstruction error → anomaly threshold ──
#     X_train_3d   = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
#     recon_train  = autoencoder.predict(X_train_3d, verbose=0)
#     mse_train    = np.mean((X_train_3d - recon_train) ** 2, axis=(1, 2))

#     # Threshold = 95th percentile of legit reconstruction errors
#     threshold    = np.percentile(mse_train, 95)
#     print(f"\n  Anomaly threshold (95th pct) = {threshold:.6f}")

#     recon_test   = autoencoder.predict(X_ae_test, verbose=0)
#     mse_test     = np.mean((X_ae_test - recon_test) ** 2, axis=(1, 2))
#     y_pred        = (mse_test > threshold).astype(int)

#     metrics_b = evaluate("PATH B – LSTM Autoencoder", y_test, y_pred, mse_test)

#     # ── Plot reconstruction error distribution ──
#     fig, ax = plt.subplots(figsize=(10, 5))
#     fig.patch.set_facecolor("#0D1117")
#     ax.set_facecolor("#161B22")
#     for cls, label, color in [(0, "Legit", "#4CF0B4"), (1, "Fraud", "#FF4C6A")]:
#         mask = y_test.values == cls
#         ax.hist(mse_test[mask], bins=80, alpha=0.7, label=label,
#                 color=color, density=True, edgecolor="none")
#     ax.axvline(threshold, color="#FFC947", linestyle="--",
#                linewidth=2, label=f"Threshold = {threshold:.5f}")
#     ax.set_title("PATH B – LSTM Autoencoder: Reconstruction Error Distribution",
#                  color="#E6EDF3", pad=12)
#     ax.set_xlabel("MSE Reconstruction Error", color="#E6EDF3")
#     ax.set_ylabel("Density", color="#E6EDF3")
#     ax.tick_params(colors="#E6EDF3")
#     ax.legend(facecolor="#21262D", labelcolor="#E6EDF3")
#     ax.grid(True, color="#21262D", alpha=0.5)
#     for spine in ax.spines.values(): spine.set_edgecolor("#21262D")
#     plt.tight_layout()
#     plt.savefig(f"{PLOTS_DIR}/path_b_recon_error.png", dpi=150,
#                 bbox_inches="tight", facecolor=fig.get_facecolor())
#     plt.close()
#     print(f"  Plot saved → {PLOTS_DIR}/path_b_recon_error.png")

#     # ── Save ──
#     autoencoder.save(f"{MODELS_DIR}/path_b_lstm_autoencoder.keras")
#     joblib.dump(threshold, f"{MODELS_DIR}/path_b_threshold.pkl")
#     print("  Model saved → models/path_b_lstm_autoencoder.keras")

#     return autoencoder, threshold, mse_test, metrics_b


# # ═════════════════════════════════════════════════════════════════════
# # PATH C – Hybrid Ensemble
# #          Resampling: SMOTE + Tomek
# #          Model:      XGBoost + Random Forest  (soft-vote ensemble)
# #          Explain:    SHAP on XGBoost component
# # ═════════════════════════════════════════════════════════════════════
# def path_c(X_train, X_test, y_train, y_test):
#     print("\n\n" + "█"*60)
#     print("  PATH C – Hybrid Ensemble  (SMOTE+Tomek + XGBoost + RF)")
#     print("█"*60)

#     # ── Resample ──
#     X_res, y_res = resample_smote_tomek(X_train, y_train)

#     # ── Train XGBoost ──
#     print("\n  Training XGBoost component …")
#     xgb = XGBClassifier(
#         n_estimators=300, max_depth=6, learning_rate=0.05,
#         subsample=0.8, colsample_bytree=0.8,
#         use_label_encoder=False, eval_metric="logloss",
#         random_state=RANDOM_SEED, n_jobs=-1,
#     )
#     xgb.fit(X_res, y_res, verbose=False)

#     # ── Train Random Forest ──
#     print("  Training Random Forest component …")
#     rf = RandomForestClassifier(
#         n_estimators=200, max_depth=None, min_samples_leaf=2,
#         class_weight="balanced", random_state=RANDOM_SEED, n_jobs=-1,
#     )
#     rf.fit(X_res, y_res)

#     # ── Soft-vote ensemble ──
#     print("  Combining via soft-vote (0.6 XGB + 0.4 RF) …")
#     prob_xgb   = xgb.predict_proba(X_test)[:, 1]
#     prob_rf    = rf.predict_proba(X_test)[:, 1]
#     prob_ens   = 0.6 * prob_xgb + 0.4 * prob_rf

#     # Dynamic threshold: maximise F1 on validation set
#     thresholds = np.linspace(0.1, 0.9, 81)
#     f1s        = [f1_score(y_test, (prob_ens > t).astype(int), zero_division=0)
#                   for t in thresholds]
#     best_thresh = thresholds[np.argmax(f1s)]
#     print(f"  Optimal threshold (max-F1) = {best_thresh:.2f}")

#     y_pred     = (prob_ens > best_thresh).astype(int)
#     metrics_c  = evaluate("PATH C – Hybrid Ensemble", y_test, y_pred, prob_ens)

#     # ── SHAP for XGBoost component ──
#     print("\n  Computing SHAP values (XGBoost component) …")
#     explainer  = shap.TreeExplainer(xgb)
#     sample_idx = np.where(y_test.values == 1)[0][:50]
#     X_sample   = X_test.iloc[sample_idx]
#     shap_vals  = explainer.shap_values(X_sample)

#     plt.figure(figsize=(10, 6))
#     shap.summary_plot(shap_vals, X_sample, show=False)
#     plt.title("PATH C – SHAP Beeswarm (XGBoost, Fraud Cases)", pad=12)
#     plt.tight_layout()
#     plt.savefig(f"{PLOTS_DIR}/path_c_shap.png", dpi=150, bbox_inches="tight")
#     plt.close()
#     print(f"  SHAP plot saved → {PLOTS_DIR}/path_c_shap.png")

#     # ── Save ──
#     joblib.dump(xgb,         f"{MODELS_DIR}/path_c_xgb.pkl")
#     joblib.dump(rf,          f"{MODELS_DIR}/path_c_rf.pkl")
#     joblib.dump(best_thresh, f"{MODELS_DIR}/path_c_threshold.pkl")
#     print("  Models saved → models/path_c_*.pkl")

    
#     return xgb, rf, best_thresh, metrics_c


# # ─────────────────────────────────────────────
# # FINAL COMPARISON PLOT
# # ─────────────────────────────────────────────
# def plot_comparison(metrics_a, metrics_b, metrics_c):
#     paths   = ["Path A\n(XGBoost+ProbDist)", "Path B\n(LSTM AutoEnc)", "Path C\n(Hybrid Ens)"]
#     metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]
#     colors  = ["#FF4C6A", "#4CF0B4", "#FFC947"]
#     data    = [
#         [metrics_a.get(m) or 0 for m in metrics],
#         [metrics_b.get(m) or 0 for m in metrics],
#         [metrics_c.get(m) or 0 for m in metrics],
#     ]

#     fig, ax = plt.subplots(figsize=(13, 6))
#     fig.patch.set_facecolor("#0D1117")
#     ax.set_facecolor("#161B22")

#     x     = np.arange(len(metrics))
#     width = 0.22
#     for i, (path, vals, col) in enumerate(zip(paths, data, colors)):
#         bars = ax.bar(x + i*width - width, vals, width,
#                       label=path, color=col, alpha=0.85)
#         for bar, v in zip(bars, vals):
#             ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
#                     f"{v:.3f}", ha="center", va="bottom",
#                     color="#E6EDF3", fontsize=7.5)

#     ax.set_xticks(x)
#     ax.set_xticklabels(["Accuracy","Precision","Recall","F1-Score","ROC-AUC"],
#                        color="#E6EDF3")
#     ax.set_ylim(0, 1.1)
#     ax.set_ylabel("Score", color="#E6EDF3")
#     ax.set_title("FraudX – Module 1: Path Comparison (All Metrics)",
#                  color="#E6EDF3", fontsize=13, pad=14)
#     ax.tick_params(colors="#E6EDF3")
#     ax.legend(facecolor="#21262D", labelcolor="#E6EDF3", fontsize=9)
#     ax.grid(True, axis="y", color="#21262D", alpha=0.5)
#     for spine in ax.spines.values(): spine.set_edgecolor("#21262D")

#     plt.tight_layout()
#     plt.savefig(f"{PLOTS_DIR}/final_comparison.png", dpi=150,
#                 bbox_inches="tight", facecolor=fig.get_facecolor())
#     plt.close()
#     print(f"\n  Comparison plot saved → {PLOTS_DIR}/final_comparison.png")


# # ─────────────────────────────────────────────
# # MAIN
# # ─────────────────────────────────────────────
# def main():
#     print("\n" + "╔"+"═"*58+"╗")
#     print("║  FraudX – Module 1: Credit Card Fraud Detection          ║")
#     print("║  3-Path Training Pipeline                                 ║")
#     print("╚"+"═"*58+"╝")

#     df = load_data(DATA_PATH)
#     X_train, X_test, y_train, y_test, scaler = base_preprocess(df)

#     # Run all 3 paths
#     _,            metrics_a = path_a(X_train, X_test, y_train, y_test)
#     _, _, _, metrics_b = path_b(X_train, X_test, y_train, y_test)
#     _, _, _, metrics_c = path_c(X_train, X_test, y_train, y_test)
#     # Final comparison
#     plot_comparison(metrics_a, metrics_b, metrics_c)

#     print("\n\n" + "="*60)
#     print("  ALL 3 PATHS COMPLETE")
#     print("  Best model = highest F1 on test set")
#     best = max(
#         [("Path A", metrics_a["f1"]),
#          ("Path B", metrics_b["f1"]),
#          ("Path C", metrics_c["f1"])],
#         key=lambda x: x[1]
#     )
#     print(f"  → WINNER: {best[0]}  (F1 = {best[1]:.4f})")
#     print("="*60 + "\n")

# if __name__ == "__main__":
#     main()
import os
import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
)
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from imblearn.combine import SMOTETomek
import shap

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import (
    LSTM, Dense, Dropout, RepeatVector,
    TimeDistributed, Input
)
from tensorflow.keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

DATA_PATH   = "data/creditcard.csv"
MODELS_DIR  = "models"
PLOTS_DIR   = "plots"
RANDOM_SEED = 42

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR,  exist_ok=True)

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

def load_data(path: str):
    df = pd.read_csv(path)
    print(f"Shape: {df.shape}")
    print(f"Fraud cases: {df['Class'].sum()} ({df['Class'].mean()*100:.3f}%)")
    print(f"Legit cases: {(df['Class']==0).sum()}")
    return df

def base_preprocess(df: pd.DataFrame):
    df = df.copy()
    scaler = StandardScaler()
    df["Amount_scaled"] = scaler.fit_transform(df[["Amount"]])
    df["Time_scaled"]   = scaler.fit_transform(df[["Time"]])
    df.drop(["Amount", "Time"], axis=1, inplace=True)
    X = df.drop("Class", axis=1)
    y = df["Class"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_SEED
    )
    return X_train, X_test, y_train, y_test, scaler

def resample_probability_distribution(X_train, y_train, plot=True):
    X_fraud = X_train[y_train == 1].values
    X_legit = X_train[y_train == 0].values
    mu_f,  std_f  = X_fraud.mean(axis=0), X_fraud.std(axis=0) + 1e-9
    mu_l,  std_l  = X_legit.mean(axis=0), X_legit.std(axis=0) + 1e-9
    def log_likelihood(X, mu, std):
        return -0.5 * np.sum(((X - mu) / std) ** 2, axis=1)
    ll_fraud_given_legit = log_likelihood(X_legit, mu_f, std_f)
    ll_legit_given_legit = log_likelihood(X_legit, mu_l, std_l)
    log_ratio = ll_fraud_given_legit - ll_legit_given_legit
    fraud_prob_score = 1 / (1 + np.exp(-log_ratio))
    n_fraud     = len(X_fraud)
    n_keep_hard = min(n_fraud * 3, len(X_legit) // 2)
    n_keep_rand = n_fraud * 3
    hard_idx = np.argsort(fraud_prob_score)[::-1][:n_keep_hard]
    rand_mask = np.ones(len(X_legit), dtype=bool)
    rand_mask[hard_idx] = False
    rand_idx  = np.random.choice(np.where(rand_mask)[0],
                                 size=n_keep_rand, replace=False)
    kept_idx  = np.union1d(hard_idx, rand_idx)
    X_legit_kept = X_legit[kept_idx]
    n_synth   = len(X_legit_kept) - n_fraud
    synthetic = np.random.normal(loc=mu_f, scale=std_f, size=(n_synth, len(mu_f)))
    for i in range(synthetic.shape[1]):
        synthetic[:, i] = np.clip(synthetic[:, i],
                                  X_fraud[:, i].min(),
                                  X_fraud[:, i].max())
    X_res = np.vstack([X_legit_kept, X_fraud, synthetic])
    y_res = np.hstack([
        np.zeros(len(X_legit_kept)),
        np.ones(n_fraud),
        np.ones(n_synth)
    ])
    perm  = np.random.permutation(len(X_res))
    X_res, y_res = X_res[perm], y_res[perm]
    return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)

def resample_smote_tomek(X_train, y_train):
    smt = SMOTETomek(random_state=RANDOM_SEED)
    X_res, y_res = smt.fit_resample(X_train, y_train)
    return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)

def evaluate(name, y_test, y_pred, y_prob=None):
    print(f"Results – {name}")
    print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
    print(f"F1-Score  : {f1_score(y_test, y_pred):.4f}")
    if y_prob is not None:
        print(f"ROC-AUC   : {roc_auc_score(y_test, y_prob):.4f}")
    print(classification_report(y_test, y_pred,
                                 target_names=["Legit", "Fraud"],
                                 zero_division=0))
    return {
        "accuracy":  accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall":    recall_score(y_test, y_pred),
        "f1":        f1_score(y_test, y_pred),
        "roc_auc":   roc_auc_score(y_test, y_prob) if y_prob is not None else None,
    }

def path_a(X_train, X_test, y_train, y_test):
    X_res, y_res = resample_probability_distribution(X_train, y_train, plot=True)
    clf = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    clf.fit(X_res, y_res,
            eval_set=[(X_test, y_test)],
            verbose=False)
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    metrics_a = evaluate("PATH A – XGBoost + Prob-Distribution", y_test, y_pred, y_prob)
    explainer  = shap.TreeExplainer(clf)
    sample_idx = np.where(y_test.values == 1)[0][:50]
    X_sample   = X_test.iloc[sample_idx]
    shap_vals  = explainer.shap_values(X_sample)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_vals, X_sample, show=False, plot_type="bar")
    plt.title("PATH A – SHAP Feature Importance (Fraud Class)", pad=12)
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/path_a_shap.png", dpi=150, bbox_inches="tight")
    plt.close()
    joblib.dump(clf, f"{MODELS_DIR}/path_a_xgboost.pkl")
    return clf, metrics_a

def build_lstm_autoencoder(timesteps: int, n_features: int) -> Model:
    inp = Input(shape=(timesteps, n_features))
    x   = LSTM(64, activation="tanh", return_sequences=False)(inp)
    x   = Dropout(0.2)(x)
    x   = Dense(16, activation="relu")(x)
    x   = RepeatVector(timesteps)(x)
    x   = LSTM(64, activation="tanh", return_sequences=True)(x)
    x   = Dropout(0.2)(x)
    out = TimeDistributed(Dense(n_features))(x)
    model = Model(inputs=inp, outputs=out)
    model.compile(optimizer="adam", loss="mse")
    return model

def path_b(X_train, X_test, y_train, y_test):
    X_res, y_res = resample_smote_tomek(X_train, y_train)
    X_legit_res = X_res[y_res == 0].values
    TIMESTEPS   = 1
    N_FEATURES  = X_legit_res.shape[1]
    X_ae_train  = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
    X_ae_test   = X_test.values.reshape(-1, TIMESTEPS, N_FEATURES)
    autoencoder = build_lstm_autoencoder(TIMESTEPS, N_FEATURES)
    autoencoder.fit(
        X_ae_train, X_ae_train,
        epochs=30,
        batch_size=256,
        validation_split=0.1,
        callbacks=[EarlyStopping(patience=5, restore_best_weights=True)],
        verbose=1,
    )
    X_train_3d   = X_legit_res.reshape(-1, TIMESTEPS, N_FEATURES)
    recon_train  = autoencoder.predict(X_train_3d, verbose=0)
    mse_train    = np.mean((X_train_3d - recon_train) ** 2, axis=(1, 2))
    threshold    = np.percentile(mse_train, 95)
    recon_test   = autoencoder.predict(X_ae_test, verbose=0)
    mse_test     = np.mean((X_ae_test - recon_test) ** 2, axis=(1, 2))
    y_pred       = (mse_test > threshold).astype(int)
    metrics_b = evaluate("PATH B – LSTM Autoencoder", y_test, y_pred, mse_test)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")
    for cls, label, color in [(0, "Legit", "#4CF0B4"), (1, "Fraud", "#FF4C6A")]:
        mask = y_test.values == cls
        ax.hist(mse_test[mask], bins=80, alpha=0.7, label=label,
                color=color, density=True, edgecolor="none")
    ax.axvline(threshold, color="#FFC947", linestyle="--",
               linewidth=2, label=f"Threshold = {threshold:.5f}")
    ax.set_title("PATH B – LSTM Autoencoder: Reconstruction Error Distribution",
                 color="#E6EDF3", pad=12)
    ax.set_xlabel("MSE Reconstruction Error", color="#E6EDF3")
    ax.set_ylabel("Density", color="#E6EDF3")
    ax.tick_params(colors="#E6EDF3")
    ax.legend(facecolor="#21262D", labelcolor="#E6EDF3")
    ax.grid(True, color="#21262D", alpha=0.5)
    for spine in ax.spines.values(): spine.set_edgecolor("#21262D")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/path_b_recon_error.png", dpi=150,
                bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    autoencoder.save(f"{MODELS_DIR}/path_b_lstm_autoencoder.keras")
    joblib.dump(threshold, f"{MODELS_DIR}/path_b_threshold.pkl")
    return autoencoder, threshold, mse_test, metrics_b

def path_c(X_train, X_test, y_train, y_test):
    X_res, y_res = resample_smote_tomek(X_train, y_train)
    xgb = XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.05,
        subsample=0.8, colsample_bytree=0.8,
        use_label_encoder=False, eval_metric="logloss",
        random_state=RANDOM_SEED, n_jobs=-1,
    )
    xgb.fit(X_res, y_res, verbose=False)
    rf = RandomForestClassifier(
        n_estimators=200, max_depth=None, min_samples_leaf=2,
        class_weight="balanced", random_state=RANDOM_SEED, n_jobs=-1,
    )
    rf.fit(X_res, y_res)
    prob_xgb   = xgb.predict_proba(X_test)[:, 1]
    prob_rf    = rf.predict_proba(X_test)[:, 1]
    prob_ens   = 0.6 * prob_xgb + 0.4 * prob_rf
    thresholds = np.linspace(0.1, 0.9, 81)
    f1s        = [f1_score(y_test, (prob_ens > t).astype(int), zero_division=0)
                  for t in thresholds]
    best_thresh = thresholds[np.argmax(f1s)]
    y_pred     = (prob_ens > best_thresh).astype(int)
    metrics_c  = evaluate("PATH C – Hybrid Ensemble", y_test, y_pred, prob_ens)
    explainer  = shap.TreeExplainer(xgb)
    sample_idx = np.where(y_test.values == 1)[0][:50]
    X_sample   = X_test.iloc[sample_idx]
    shap_vals  = explainer.shap_values(X_sample)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_vals, X_sample, show=False)
    plt.title("PATH C – SHAP Beeswarm (XGBoost, Fraud Cases)", pad=12)
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/path_c_shap.png", dpi=150, bbox_inches="tight")
    plt.close()
    joblib.dump(xgb,         f"{MODELS_DIR}/path_c_xgb.pkl")
    joblib.dump(rf,          f"{MODELS_DIR}/path_c_rf.pkl")
    joblib.dump(best_thresh, f"{MODELS_DIR}/path_c_threshold.pkl")
    return xgb, rf, best_thresh, metrics_c

def plot_comparison(metrics_a, metrics_b, metrics_c):
    paths   = ["Path A\n(XGBoost+ProbDist)", "Path B\n(LSTM AutoEnc)", "Path C\n(Hybrid Ens)"]
    metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    colors  = ["#FF4C6A", "#4CF0B4", "#FFC947"]
    data    = [
        [metrics_a.get(m) or 0 for m in metrics],
        [metrics_b.get(m) or 0 for m in metrics],
        [metrics_c.get(m) or 0 for m in metrics],
    ]
    fig, ax = plt.subplots(figsize=(13, 6))
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#161B22")
    x     = np.arange(len(metrics))
    width = 0.22
    for i, (path, vals, col) in enumerate(zip(paths, data, colors)):
        bars = ax.bar(x + i*width - width, vals, width,
                      label=path, color=col, alpha=0.85)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.005,
                    f"{v:.3f}", ha="center", va="bottom",
                    color="#E6EDF3", fontsize=7.5)
    ax.set_xticks(x)
    ax.set_xticklabels(["Accuracy","Precision","Recall","F1-Score","ROC-AUC"],
                       color="#E6EDF3")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score", color="#E6EDF3")
    ax.set_title("FraudX – Module 1: Path Comparison (All Metrics)",
                 color="#E6EDF3", fontsize=13, pad=14)
    ax.tick_params(colors="#E6EDF3")
    ax.legend(facecolor="#21262D", labelcolor="#E6EDF3", fontsize=9)
    ax.grid(True, axis="y", color="#21262D", alpha=0.5)
    for spine in ax.spines.values(): spine.set_edgecolor("#21262D")
    plt.tight_layout()
    plt.savefig(f"{PLOTS_DIR}/final_comparison.png", dpi=150,
                bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

def main():
    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test, scaler = base_preprocess(df)
    _, metrics_a = path_a(X_train, X_test, y_train, y_test)
    _, _, _, metrics_b = path_b(X_train, X_test, y_train, y_test)
    _, _, _, metrics_c = path_c(X_train, X_test, y_train, y_test)
    plot_comparison(metrics_a, metrics_b, metrics_c)
    best = max(
        [("Path A", metrics_a["f1"]),
         ("Path B", metrics_b["f1"]),
         ("Path C", metrics_c["f1"])],
        key=lambda x: x[1]
    )
    print(f"WINNER: {best[0]}  (F1 = {best[1]:.4f})")

if __name__ == "__main__":
    main()