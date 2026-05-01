"""
=============================================================
 AI-Based Smart Agriculture Crop Recommendation System
 train_model.py  –  Model Training Script
=============================================================
Run this file ONCE before starting the Flask app:
    python train_model.py

It will:
  1. Load (or generate) the dataset
  2. Pre-process the data
  3. Train a RandomForestClassifier
  4. Evaluate accuracy
  5. Save the trained model to  'model/crop_model.pkl'
     and the label encoder to  'model/label_encoder.pkl'
=============================================================
"""

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no GUI needed)
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

# ─────────────────────────────────────────────────────────────
# 1.  PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATASET     = os.path.join(BASE_DIR, "Crop_Recommendation.csv")
MODEL_DIR   = os.path.join(BASE_DIR, "model")
STATIC_DIR  = os.path.join(BASE_DIR, "static", "charts")

os.makedirs(MODEL_DIR,  exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# 2.  LOAD DATA
# ─────────────────────────────────────────────────────────────
print("[INFO] Loading dataset …")
df = pd.read_csv(DATASET)
print(f"[INFO] Dataset shape : {df.shape}")
print(df.head())

# ─────────────────────────────────────────────────────────────
# 3.  PRE-PROCESS
# ─────────────────────────────────────────────────────────────
features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
target   = "label"

X = df[features].values
y = df[target].values

# Encode crop names → integers
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train / Test split (80 / 20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.20, random_state=42, stratify=y_encoded
)
print(f"[INFO] Train size: {X_train.shape[0]}  |  Test size: {X_test.shape[0]}")

# ─────────────────────────────────────────────────────────────
# 4.  TRAIN MODEL
# ─────────────────────────────────────────────────────────────
print("[INFO] Training RandomForestClassifier …")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("[INFO] Training complete.")

# ─────────────────────────────────────────────────────────────
# 5.  EVALUATE
# ─────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"\n[RESULT] Accuracy : {acc * 100:.2f}%\n")
print("[RESULT] Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# ─────────────────────────────────────────────────────────────
# 6.  VISUALISATIONS
# ─────────────────────────────────────────────────────────────

# --- 6a. Feature Importance Bar Chart ---
importances = model.feature_importances_
feat_series = pd.Series(importances, index=features).sort_values(ascending=False)

plt.figure(figsize=(9, 5))
colors = ["#4CAF50", "#8BC34A", "#CDDC39", "#FFC107", "#FF9800", "#F44336", "#9C27B0"]
bars = plt.bar(feat_series.index, feat_series.values, color=colors, edgecolor="white", linewidth=0.8)
plt.title("Feature Importance — Crop Recommendation Model", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Feature", fontsize=12)
plt.ylabel("Importance Score", fontsize=12)
plt.xticks(fontsize=11)
for bar, val in zip(bars, feat_series.values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002,
             f"{val:.3f}", ha="center", va="bottom", fontsize=9, color="#333333")
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "feature_importance.png"), dpi=150)
plt.close()
print("[INFO] Saved feature_importance.png")

# --- 6b. Crop Count Distribution ---
crop_counts = df["label"].value_counts()
plt.figure(figsize=(12, 5))
bars2 = plt.bar(crop_counts.index, crop_counts.values,
                color=plt.cm.Set3(np.linspace(0, 1, len(crop_counts))),
                edgecolor="white", linewidth=0.8)
plt.title("Number of Samples per Crop", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Crop", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=10)
for bar, val in zip(bars2, crop_counts.values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
             str(val), ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "crop_distribution.png"), dpi=150)
plt.close()
print("[INFO] Saved crop_distribution.png")

# --- 6c. Confusion Matrix (first 8 crops for readability) ---
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(14, 11))
sns.heatmap(cm, annot=True, fmt="d", cmap="YlGn",
            xticklabels=le.classes_, yticklabels=le.classes_,
            linewidths=0.5, linecolor="white")
plt.title("Confusion Matrix", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Predicted", fontsize=12)
plt.ylabel("Actual", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=9)
plt.yticks(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(STATIC_DIR, "confusion_matrix.png"), dpi=150)
plt.close()
print("[INFO] Saved confusion_matrix.png")

# ─────────────────────────────────────────────────────────────
# 7.  SAVE MODEL & ENCODER
# ─────────────────────────────────────────────────────────────
model_path   = os.path.join(MODEL_DIR, "crop_model.pkl")
encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(encoder_path, "wb") as f:
    pickle.dump(le, f)

print(f"\n[INFO] Model saved  ->  {model_path}")
print(f"[INFO] Encoder saved ->  {encoder_path}")
print("\n[DONE] All done! You can now run:  python app.py")
