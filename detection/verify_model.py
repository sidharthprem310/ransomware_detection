import joblib
import numpy as np
import pandas as pd
import os
from sklearn.metrics import (
    classification_report, confusion_matrix,
    precision_score, recall_score, f1_score, accuracy_score
)
from sklearn.model_selection import train_test_split
from numpy.random import RandomState

model  = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

print("=" * 55)
print("   SHELL 2 — MODEL VERIFICATION & FULL METRICS REPORT")
print("=" * 55)

rng = RandomState(42)
n = 5000
n_benign    = int(0.70 * n)
n_malicious = n - n_benign

be = rng.normal(4.2, 0.85, n_benign)
hi = rng.random(n_benign) < 0.06
be[hi] = rng.uniform(5.5, 7.2, hi.sum())
br = rng.poisson(0.5, n_benign)
ba = rng.normal(2.8, 2.2, n_benign)

me = rng.normal(6.75, 0.55, n_malicious)
pm = rng.random(n_malicious) < 0.08
me[pm] = rng.uniform(5.2, 6.4, pm.sum())
mr = rng.poisson(3.5, n_malicious)
ma = rng.normal(6.2, 2.8, n_malicious)

df = pd.DataFrame({
    'entropy':       np.concatenate([be, me]),
    'rename_freq':   np.concatenate([br, mr]),
    'file_activity': np.concatenate([ba, ma]),
    'label':         np.concatenate([np.zeros(n_benign, int), np.ones(n_malicious, int)])
})
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df['entropy']       = df['entropy'].clip(0, 8)
df['rename_freq']   = df['rename_freq'].clip(0)
df['file_activity'] = df['file_activity'].clip(0)

X = df[['entropy', 'rename_freq', 'file_activity']]
y = df['label']

_, X_test, _, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
X_test_s = scaler.transform(X_test)
y_pred   = model.predict(X_test_s)

print("\n--- PER-CLASS METRICS ---")
print(classification_report(y_test, y_pred, target_names=['Benign (0)', 'Ransomware (1)'], digits=4))

print("--- SUMMARY ---")
print(f"  Overall accuracy    : {accuracy_score(y_test, y_pred):.4f}")
print(f"  Class 0 precision   : {precision_score(y_test, y_pred, pos_label=0):.4f}")
print(f"  Class 0 recall      : {recall_score(y_test, y_pred, pos_label=0):.4f}")
print(f"  Class 0 f1-score    : {f1_score(y_test, y_pred, pos_label=0):.4f}")
print(f"  Class 1 precision   : {precision_score(y_test, y_pred, pos_label=1):.4f}  <- target >= 0.94")
print(f"  Class 1 recall      : {recall_score(y_test, y_pred, pos_label=1):.4f}")
print(f"  Class 1 f1-score    : {f1_score(y_test, y_pred, pos_label=1):.4f}")

cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
print(f"\n--- CONFUSION MATRIX ---")
print(f"              Predicted 0   Predicted 1")
print(f"  Actual 0      {tn:5d}         {fp:5d}   (benign files)")
print(f"  Actual 1      {fn:5d}         {tp:5d}   (ransomware)")
print(f"\n  True Negatives  (TN): {tn}  — benign correctly identified")
print(f"  False Positives (FP): {fp}  — benign files falsely flagged as ransomware")
print(f"  False Negatives (FN): {fn}  — ransomware missed")
print(f"  True Positives  (TP): {tp}  — ransomware correctly caught")

print(f"\n--- SAVED ARTIFACTS ---")
for f in ["model.pkl", "scaler.pkl", "confusion_matrix.png", "entropy_trend.png", "entropy_attack.png"]:
    size = os.path.getsize(f) if os.path.exists(f) else 0
    ok   = "OK" if size > 0 else "MISSING"
    print(f"  {f:<30s}  {size:>8,} bytes  [{ok}]")

print("\n" + "=" * 55)