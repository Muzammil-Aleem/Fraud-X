# import os
# import re
# import warnings
# import numpy as np
# import pandas as pd
# import joblib
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# warnings.filterwarnings("ignore")

# for pkg in ["stopwords", "wordnet", "omw-1.4"]:
#     nltk.download(pkg, quiet=True)

# os.makedirs("models", exist_ok=True)

# def load_data():
#     frames = []

#     if os.path.exists("data/Fake.csv") and os.path.exists("data/True.csv"):
#         fake = pd.read_csv("data/Fake.csv")
#         true = pd.read_csv("data/True.csv")
#         fake["label"] = 0
#         true["label"] = 1
#         for df in [fake, true]:
#             df["content"] = (
#                 df.get("title", pd.Series([""] * len(df))).fillna("").astype(str)
#                 + " "
#                 + df.get("text", pd.Series([""] * len(df))).fillna("").astype(str)
#             )
#         frames.append(pd.concat([fake, true])[["content", "label"]])
#         print(f"  Bisaillon  → {len(fake)} fake + {len(true)} real")

#     if os.path.exists("data/news.csv"):
#         noyan = pd.read_csv("data/news.csv")
#         if "label" in noyan.columns:
#             noyan["label"] = noyan["label"].map({"FAKE": 0, "REAL": 1, 0: 0, 1: 1})
#         noyan["content"] = noyan.get("text", noyan.iloc[:, 0]).fillna("").astype(str)
#         noyan = noyan[["content", "label"]].dropna()
#         frames.append(noyan)
#         print(f"  Noyan      → {len(noyan)} articles")

#     if os.path.exists("data/WELFake_Dataset.csv"):
#         sau = pd.read_csv("data/WELFake_Dataset.csv")
#         sau["label"] = sau["label"].astype(int)
#         sau["content"] = (
#             sau.get("title", pd.Series([""] * len(sau))).fillna("").astype(str)
#             + " "
#             + sau.get("text", pd.Series([""] * len(sau))).fillna("").astype(str)
#         )
#         frames.append(sau[["content", "label"]].dropna())
#         print(f"  Saurabhshahane → {len(sau)} articles")

#     if not frames:
#         raise FileNotFoundError(
#             "No datasets found. Place Fake.csv & True.csv in the data/ folder."
#         )

#     data = pd.concat(frames, ignore_index=True)
#     data = data.dropna(subset=["content", "label"])
#     data["label"] = data["label"].astype(int)
#     print(f"\n  Total corpus: {len(data)} articles  |  "
#           f"Fake: {(data['label']==0).sum()}  Real: {(data['label']==1).sum()}\n")
#     return data


# _lemmatizer = WordNetLemmatizer()
# _stop_words  = set(stopwords.words("english"))

# def preprocess(text: str) -> str:
#     text = text.lower()
#     text = re.sub(r"http\S+|www\S+", " ", text)       
#     text = re.sub(r"[^a-z\s]", " ", text)              
#     text = re.sub(r"\s+", " ", text).strip()
#     tokens = [
#         _lemmatizer.lemmatize(w)
#         for w in text.split()
#         if w not in _stop_words and len(w) > 2
#     ]
#     return " ".join(tokens)

# from sklearn.metrics import (accuracy_score, precision_score,
#                               recall_score, f1_score,
#                               roc_auc_score, classification_report)

# def evaluate(name, y_true, y_pred, y_prob=None):
#     print(f"\n  {'─'*52}")
#     print(f"  {name}")
#     print(f"  {'─'*52}")
#     print(f"  Accuracy : {accuracy_score(y_true, y_pred):.4f}")
#     print(f"  Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
#     print(f"  Recall   : {recall_score(y_true, y_pred, zero_division=0):.4f}")
#     print(f"  F1-Score : {f1_score(y_true, y_pred, zero_division=0):.4f}")
#     if y_prob is not None:
#         print(f"  ROC-AUC  : {roc_auc_score(y_true, y_prob):.4f}")
#     print()
#     print(classification_report(y_true, y_pred,
#                                 target_names=["Fake", "Real"], zero_division=0))
#     return f1_score(y_true, y_pred, zero_division=0)


# def train_path_a(X_train, X_test, y_train, y_test):
#     from sklearn.feature_extraction.text import TfidfVectorizer
#     from sklearn.svm import LinearSVC
#     from sklearn.naive_bayes import MultinomialNB
#     from sklearn.linear_model import LogisticRegression
#     from sklearn.calibration import CalibratedClassifierCV
#     from xgboost import XGBClassifier

#     print("  PATH A  —  TF-IDF + Classical ML")
    
#     vectorizer = TfidfVectorizer(
#         stop_words="english",
#         max_features=50000,          
#         ngram_range=(1, 2),          
#         sublinear_tf=True,          
#         min_df=3,
#         max_df=0.90
#     )
#     X_train_vec = vectorizer.fit_transform(X_train)
#     X_test_vec  = vectorizer.transform(X_test)

#     best_f1    = 0
#     best_model = None
#     best_name  = ""

#     xgb = XGBClassifier(
#         n_estimators=300,
#         max_depth=6,
#         learning_rate=0.1,
#         subsample=0.8,
#         colsample_bytree=0.8,
#         use_label_encoder=False,
#         eval_metric="logloss",
#         random_state=42,
#         n_jobs=-1
#     )
#     xgb.fit(X_train_vec, y_train)
#     pred  = xgb.predict(X_test_vec)
#     prob  = xgb.predict_proba(X_test_vec)[:, 1]
#     f1    = evaluate("A1 — XGBoost", y_test, pred, prob)
#     if f1 > best_f1:
#         best_f1, best_model, best_name = f1, xgb, "XGBoost"

#     svm_base = LinearSVC(C=1.0, max_iter=2000, random_state=42)
#     svm      = CalibratedClassifierCV(svm_base, cv=3)  
#     svm.fit(X_train_vec, y_train)
#     pred = svm.predict(X_test_vec)
#     prob = svm.predict_proba(X_test_vec)[:, 1]
#     f1   = evaluate("A2 — Linear SVM", y_test, pred, prob)
#     if f1 > best_f1:
#         best_f1, best_model, best_name = f1, svm, "LinearSVM"

#     nb   = MultinomialNB(alpha=0.1)
#     nb.fit(X_train_vec, y_train)
#     pred = nb.predict(X_test_vec)
#     prob = nb.predict_proba(X_test_vec)[:, 1]
#     f1   = evaluate("A3 — Naive Bayes", y_test, pred, prob)
#     if f1 > best_f1:
#         best_f1, best_model, best_name = f1, nb, "NaiveBayes"

#     print(f"\n  ✔  Path A winner: {best_name}  (F1 = {best_f1:.4f})")
#     joblib.dump(best_model,  "models/path_a_model.pkl")
#     joblib.dump(vectorizer,  "models/vectorizer.pkl")        
#     joblib.dump(best_model,  "models/fake_model.pkl")         
#     print("  Saved → models/path_a_model.pkl, models/vectorizer.pkl, models/fake_model.pkl")
#     return vectorizer, best_model


# def train_path_b(X_train_raw, X_test_raw, y_train, y_test):
#     from gensim.models import Word2Vec
#     from sklearn.svm import SVC
#     from sklearn.calibration import CalibratedClassifierCV
#     from xgboost import XGBClassifier

#     print("  PATH B  —  Word Embeddings + ML Classifiers")
    
#     train_tokens = [t.split() for t in X_train_raw]
#     test_tokens  = [t.split() for t in X_test_raw]

#     print("  Training Word2Vec (this may take a minute)…")
#     w2v = Word2Vec(
#         sentences=train_tokens,
#         vector_size=200,
#         window=5,
#         min_count=2,
#         workers=4,
#         epochs=10,
#         sg=1               
#     )
#     w2v.save("models/word2vec.model")
#     print("  Word2Vec trained. Vocabulary size:", len(w2v.wv))

#     def doc_vector(tokens, model, dim=200):
#         vecs = [model.wv[w] for w in tokens if w in model.wv]
#         return np.mean(vecs, axis=0) if vecs else np.zeros(dim)

#     X_train_w2v = np.array([doc_vector(t, w2v) for t in train_tokens])
#     X_test_w2v  = np.array([doc_vector(t, w2v) for t in test_tokens])

#     best_f1    = 0
#     best_model = None
#     best_name  = ""
#     best_Xtr   = None
#     best_Xte   = None

#     xgb = XGBClassifier(
#         n_estimators=300,
#         max_depth=6,
#         learning_rate=0.1,
#         random_state=42,
#         n_jobs=-1,
#         eval_metric="logloss"
#     )
#     xgb.fit(X_train_w2v, y_train)
#     pred = xgb.predict(X_test_w2v)
#     prob = xgb.predict_proba(X_test_w2v)[:, 1]
#     f1   = evaluate("B1 — Word2Vec + XGBoost", y_test, pred, prob)
#     if f1 > best_f1:
#         best_f1, best_model, best_name = f1, xgb, "Word2Vec+XGBoost"
#         best_Xtr, best_Xte = X_train_w2v, X_test_w2v

#     svm_base = SVC(kernel="rbf", C=1.0, probability=True, random_state=42)
#     svm_base.fit(X_train_w2v, y_train)
#     pred = svm_base.predict(X_test_w2v)
#     prob = svm_base.predict_proba(X_test_w2v)[:, 1]
#     f1   = evaluate("B2 — Word2Vec + SVM (RBF)", y_test, pred, prob)
#     if f1 > best_f1:
#         best_f1, best_model, best_name = f1, svm_base, "Word2Vec+SVM"
#         best_Xtr, best_Xte = X_train_w2v, X_test_w2v

#     glove_path = "data/glove.6B.200d.txt"
#     if os.path.exists(glove_path):
#         print("\n  Loading GloVe embeddings…")
#         glove = {}
#         with open(glove_path, "r", encoding="utf-8") as f:
#             for line in f:
#                 parts = line.split()
#                 glove[parts[0]] = np.array(parts[1:], dtype=np.float32)
#         print(f"  GloVe loaded. Vocab size: {len(glove)}")

#         def glove_vector(tokens, dim=200):
#             vecs = [glove[w] for w in tokens if w in glove]
#             return np.mean(vecs, axis=0) if vecs else np.zeros(dim)

#         X_train_glv = np.array([glove_vector(t) for t in train_tokens])
#         X_test_glv  = np.array([glove_vector(t) for t in test_tokens])

#         xgb_glv = XGBClassifier(
#             n_estimators=300, max_depth=6, learning_rate=0.1,
#             random_state=42, n_jobs=-1, eval_metric="logloss"
#         )
#         xgb_glv.fit(X_train_glv, y_train)
#         pred = xgb_glv.predict(X_test_glv)
#         prob = xgb_glv.predict_proba(X_test_glv)[:, 1]
#         f1   = evaluate("B3 — GloVe + XGBoost", y_test, pred, prob)
#         if f1 > best_f1:
#             best_f1, best_model, best_name = f1, xgb_glv, "GloVe+XGBoost"
#             best_Xtr, best_Xte = X_train_glv, X_test_glv
#     else:
#         print("\n  GloVe file not found at data/glove.6B.200d.txt — skipping B3.")
#         print("  Download from: https://nlp.stanford.edu/data/glove.6B.zip")

#     print(f"\n  ✔  Path B winner: {best_name}  (F1 = {best_f1:.4f})")
#     joblib.dump(best_model, "models/path_b_model.pkl")
#     joblib.dump(w2v,        "models/word2vec.model")
#     print("  Saved → models/path_b_model.pkl, models/word2vec.model")
#     return w2v, best_model


# def train_path_c(X_train_raw, X_test_raw, y_train, y_test,
#                  model_name="albert-base-v2", epochs=3, batch_size=16):
#     try:
#         import torch
#         from torch.utils.data import Dataset, DataLoader
#         from transformers import AutoTokenizer, AutoModelForSequenceClassification
#         from torch.optim import AdamW
#         from transformers import get_linear_schedule_with_warmup

#     except ImportError:
#         print("\n PyTorch / Transformers not installed.")
#         print("     Run:  pip install torch transformers")
#         print("  Skipping Path C.\n")
#         return None, None

    
#     print(f"  PATH C  —  Transformer: {model_name}")
    
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print(f"  Device: {device}")

#     MAX_LEN = 64

#     class NewsDataset(Dataset):
#         def __init__(self, texts, labels, tokenizer):
#             self.encodings = tokenizer(
#                 list(texts),
#                 truncation=True,
#                 padding="max_length",
#                 max_length=MAX_LEN,
#                 return_tensors="pt"
#             )
#             self.labels = torch.tensor(list(labels), dtype=torch.long)

#         def __len__(self):
#             return len(self.labels)

#         def __getitem__(self, idx):
#             return {
#                 "input_ids":      self.encodings["input_ids"][idx],
#                 "attention_mask": self.encodings["attention_mask"][idx],
#                 "labels":         self.labels[idx]
#             }

#     print(f"  Loading tokenizer and model from HuggingFace…")
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model     = AutoModelForSequenceClassification.from_pretrained(
#         model_name, num_labels=2
#     )
#     model.to(device)

#     train_ds = NewsDataset(X_train_raw, y_train, tokenizer)
#     test_ds  = NewsDataset(X_test_raw,  y_test,  tokenizer)
#     train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
#     test_dl  = DataLoader(test_ds,  batch_size=batch_size)

#     optimizer = AdamW(model.parameters(), lr=2e-5, weight_decay=0.01)
#     total_steps = len(train_dl) * epochs
#     scheduler = get_linear_schedule_with_warmup(
#         optimizer,
#         num_warmup_steps=int(0.1 * total_steps),
#         num_training_steps=total_steps
#     )

#     for epoch in range(epochs):
#         model.train()
#         total_loss = 0
#         for batch in train_dl:
#             optimizer.zero_grad()
#             outputs = model(
#                 input_ids=batch["input_ids"].to(device),
#                 attention_mask=batch["attention_mask"].to(device),
#                 labels=batch["labels"].to(device)
#             )
#             loss = outputs.loss
#             loss.backward()
#             torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
#             optimizer.step()
#             scheduler.step()
#             total_loss += loss.item()
#         avg_loss = total_loss / len(train_dl)
#         print(f"  Epoch {epoch+1}/{epochs}  |  Loss: {avg_loss:.4f}")

#     model.eval()
#     all_preds, all_probs, all_labels = [], [], []
#     with torch.no_grad():
#         for i, batch in enumerate(test_dl):
#             if i % 50 == 0:
#                 print(f"Batch {i}/{len(train_dl)} processed")
#             outputs = model(
#                     input_ids=batch["input_ids"].to(device),
#                 attention_mask=batch["attention_mask"].to(device)
#             )
#             logits = outputs.logits
#             probs  = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
#             preds  = torch.argmax(logits, dim=1).cpu().numpy()
#             all_preds.extend(preds)
#             all_probs.extend(probs)
#             all_labels.extend(batch["labels"].numpy())

#     short = model_name.split("/")[-1].upper()
#     evaluate(f"C — {short}", all_labels, all_preds, all_probs)

#     safe_name = model_name.replace("/", "_").replace("-", "_")
#     save_dir  = f"models/path_c_{safe_name}"
#     model.save_pretrained(save_dir)
#     tokenizer.save_pretrained(save_dir)
#     print(f"  Saved → {save_dir}/")
#     return tokenizer, model


# if __name__ == "__main__":
#     from sklearn.model_selection import train_test_split

#     print("Loading datasets…")
#     data = load_data()

#     print("Preprocessing text (tokenize → lemmatize)…")
#     data["clean"] = data["content"].apply(preprocess)
#     data = data[data["clean"].str.strip().astype(bool)]     

#     X_raw   = data["clean"].to_numpy()
#     y       = data["label"].to_numpy()
#     X_train, X_test, y_train, y_test = train_test_split(
#         X_raw, y, test_size=0.20, random_state=42, stratify=y
#     )
#     print(f"  Train: {len(X_train)}   Test: {len(X_test)}\n")

#     # vectorizer, path_a_model = train_path_a(X_train, X_test, y_train, y_test)

#     # w2v_model, path_b_model = train_path_b(X_train, X_test, y_train, y_test)

#     train_path_c(X_train, X_test, y_train, y_test,
#                  model_name="albert-base-v2", epochs=3, batch_size=16)

#     # train_path_c(X_train, X_test, y_train, y_test,
#     #              model_name="bert-base-uncased", epochs=3, batch_size=16)

#     # train_path_c(X_train, X_test, y_train, y_test,
#     #              model_name="roberta-base", epochs=3, batch_size=16)

#     print("  ALL PATHS COMPLETE")
#     print("  Saved models:")
#     print("    models/fake_model.pkl      ← default for app.py (Path A best)")
#     print("    models/vectorizer.pkl      ← TF-IDF vectorizer")
#     print("    models/path_a_model.pkl    ← Path A best classifier")
#     print("    models/path_b_model.pkl    ← Path B best classifier")
#     print("    models/word2vec.model      ← Word2Vec embeddings")
#     print("    models/path_c_albert_*/    ← Fine-tuned ALBERT")


import os
import re
import warnings
import pandas as pd
import joblib
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)

warnings.filterwarnings("ignore")

for pkg in ["stopwords", "wordnet", "omw-1.4"]:
    nltk.download(pkg, quiet=True)

os.makedirs("models", exist_ok=True)

print("Loading datasets...")

fake_df = pd.read_csv("data/Fake.csv")
true_df = pd.read_csv("data/True.csv")

fake_df["label"] = 0
true_df["label"] = 1

fake_df["content"] = (
    fake_df["title"].fillna("") + " " +
    fake_df["text"].fillna("")
)

true_df["content"] = (
    true_df["title"].fillna("") + " " +
    true_df["text"].fillna("")
)

fake_df = fake_df[["content", "label"]]
true_df = true_df[["content", "label"]]

data = pd.concat([fake_df, true_df], ignore_index=True)

data.dropna(inplace=True)

print(f"Fake News Articles : {len(fake_df)}")
print(f"Real News Articles : {len(true_df)}")
print(f"Total Dataset Size : {len(data)}")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess(text):
    text = str(text).lower()

    text = re.sub(r"http\S+|www\S+", " ", text)

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    tokens = [
        lemmatizer.lemmatize(word)
        for word in text.split()
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(tokens)

print("\nPreprocessing text...")
data["clean"] = data["content"].apply(preprocess)

data = data[data["clean"].str.strip().astype(bool)]

X = data["clean"]
y = data["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"\nTraining Samples : {len(X_train)}")
print(f"Testing Samples  : {len(X_test)}")

vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    ngram_range=(1, 3),
    max_features=50000,
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("\nTraining Naive Bayes Model...")

model = MultinomialNB(alpha=0.1)

model.fit(X_train_vec, y_train)

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
        target_names=["Fake", "Real"],
        zero_division=0
    )
)

joblib.dump(model, "models/fake_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")