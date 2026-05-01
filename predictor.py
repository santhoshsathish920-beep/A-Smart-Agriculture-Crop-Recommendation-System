"""
=============================================================
 predictor.py  —  ML Prediction Engine
=============================================================
 Loads the trained RandomForestClassifier and provides:
   predict_top3()  —  returns top 3 predicted crops
                       with confidence scores and full info
=============================================================
"""

import os
import pickle
import numpy as np

from config      import CROP_INFO, PRICE_UNIT, MAX_PRICE
from recommendations import (
    get_fertilizer_tip,
    get_soil_health_tip,
    get_rotation_suggestion,
)

# ── Load Model & Encoder once at import time ─────────────
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH   = os.path.join(BASE_DIR, "model", "crop_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "model", "label_encoder.pkl")

print("[predictor] Loading model …")
with open(MODEL_PATH, "rb") as f:
    _model = pickle.load(f)

with open(ENCODER_PATH, "rb") as f:
    _label_encoder = pickle.load(f)

print(f"[predictor] Ready. Classes: {list(_label_encoder.classes_)}")


def get_all_crops() -> list:
    """Return sorted list of all crop names from the label encoder."""
    return sorted([c.title() for c in _label_encoder.classes_])


def predict_top3(n: float, p: float, k: float,
                 temperature: float, humidity: float,
                 ph: float, rainfall: float) -> dict:
    """
    Run Random Forest prediction and return top-3 crops.

    Args:
        n, p, k        : soil NPK values (mg/kg)
        temperature    : average temperature (°C)
        humidity       : relative humidity (%)
        ph             : soil pH
        rainfall       : average rainfall (mm)

    Returns dict with keys:
        top3          : list of 3 dicts (ranked by confidence)
        soil_health   : soil diagnosis dict
        crops_list    : all crop names (for dynamic UI display)
    """
    features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

    # Get probability scores for every class
    proba_all = _model.predict_proba(features)[0]   # shape: (n_classes,)

    # Sort classes by probability descending, take top 3
    top_indices = np.argsort(proba_all)[::-1][:3]

    top3 = []
    for rank, idx in enumerate(top_indices):
        crop_raw    = _label_encoder.inverse_transform([idx])[0]   # e.g. "rice"
        confidence  = round(float(proba_all[idx]) * 100, 1)
        info        = CROP_INFO.get(crop_raw, {})
        price       = info.get("price", 0)
        fert        = get_fertilizer_tip(crop_raw)
        rotation    = get_rotation_suggestion(crop_raw)

        # Relative profitability as percentage of the most expensive crop
        profit_pct  = round(price / MAX_PRICE * 100)

        top3.append({
            "rank":        rank + 1,
            "crop":        crop_raw.title(),          # "Rice"
            "crop_raw":    crop_raw,                  # "rice"
            "confidence":  confidence,
            "icon":        info.get("icon", "🌱"),
            "season":      info.get("season", "—"),
            "water":       info.get("water", "—"),
            "duration":    info.get("duration", "—"),
            "price":       price,
            "price_unit":  PRICE_UNIT,
            "profit_pct":  profit_pct,
            "fertilizer":  fert,
            "rotation":    rotation,
        })

    # Soil health diagnosis (uses raw N/P/K/pH values from user)
    soil_health = get_soil_health_tip(ph, n, p, k)

    # All crops list for dynamic display in the UI
    crops_list = get_all_crops()

    return {
        "top3":        top3,
        "soil_health": soil_health,
        "crops_list":  crops_list,
    }
