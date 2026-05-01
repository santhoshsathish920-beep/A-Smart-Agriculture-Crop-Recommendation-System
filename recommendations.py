"""
=============================================================
 recommendations.py  —  Expert Advisory Engine
=============================================================
 Rule-based recommendations for:
   1. Fertilizer (NPK ratios + product tips)
   2. Soil Health (based on pH, N, P, K values)
   3. Crop Rotation (what to grow next season)
=============================================================
"""

# ── Fertilizer Tips ───────────────────────────────────────
# Per crop: recommended fertilizer schedule & key products
FERTILIZER_DB = {
    "rice":        {"npk": "80:40:40",  "tip": "Apply Urea at tillering stage. Use DAP as basal dose. Add Zinc Sulphate for micronutrients.",         "products": ["Urea", "DAP", "Zinc Sulphate"]},
    "maize":       {"npk": "120:60:40", "tip": "Split Nitrogen in 3 doses (basal, knee-high, tasseling). Use MOP for Potassium.",                      "products": ["Urea", "SSP", "MOP"]},
    "chickpea":    {"npk": "20:60:20",  "tip": "Low N needed (fixes own N). Apply Rhizobium seed treatment. Use SSP for phosphorus.",                  "products": ["DAP", "SSP", "Rhizobium"]},
    "kidneybeans": {"npk": "20:60:60",  "tip": "Use Rhizobium inoculant. Apply phosphorus and potassium as basal. Avoid excess nitrogen.",              "products": ["DAP", "MOP", "Rhizobium"]},
    "pigeonpeas":  {"npk": "20:50:20",  "tip": "Apply basal P and K. Nitrogen fixing crop — minimal N needed. Use Sulphur for yield boost.",            "products": ["SSP", "MOP", "Sulphur"]},
    "mothbeans":   {"npk": "20:40:20",  "tip": "Drought-tolerant — light fertilization. Apply basal DAP. No extra N required.",                         "products": ["DAP", "SSP"]},
    "mungbean":    {"npk": "20:40:20",  "tip": "Apply DAP at sowing. Use Rhizobium culture for N fixation. Avoid waterlogging.",                        "products": ["DAP", "Rhizobium", "Zinc Sulphate"]},
    "blackgram":   {"npk": "20:40:20",  "tip": "Seed treat with Rhizobium. Apply P & K as basal. Top dress with low N if needed.",                      "products": ["SSP", "MOP", "Rhizobium"]},
    "lentil":      {"npk": "15:60:20",  "tip": "Use Rhizobium seed treatment. High phosphorus improves yield. Apply Sulphur for protein content.",      "products": ["DAP", "Sulphur", "Rhizobium"]},
    "pomegranate": {"npk": "50:25:50",  "tip": "Apply fertilizer in split doses (June, Oct). Use micronutrient mix (Boron + Zinc).",                    "products": ["Urea", "SSP", "MOP", "Boron"]},
    "banana":      {"npk": "200:60:200","tip": "Heavy feeder — apply in monthly splits. Drip fertigation is ideal. Add Magnesium for leaf health.",      "products": ["Urea", "MOP", "Magnesium Sulphate"]},
    "mango":       {"npk": "100:50:100","tip": "Apply before monsoon and after harvest. Use micronutrients (Zinc, Boron). Avoid N before flowering.",    "products": ["Urea", "SSP", "MOP", "Zinc"]},
    "grapes":      {"npk": "100:50:75", "tip": "Apply N in splits. Potassium essential for fruit quality. Use Calcium Nitrate near harvest.",            "products": ["Urea", "MOP", "Calcium Nitrate"]},
    "watermelon":  {"npk": "80:60:60",  "tip": "Apply basal N:P:K. Side-dress Urea at vine development. Add Boron for fruit set.",                      "products": ["Urea", "DAP", "MOP", "Boron"]},
    "muskmelon":   {"npk": "60:50:50",  "tip": "Apply P and K basally. Side-dress N at fruit development. Calcium spray prevents blossom-end rot.",      "products": ["Urea", "SSP", "MOP"]},
    "apple":       {"npk": "70:35:70",  "tip": "Apply N in early spring. K is critical for fruit colour. Use foliar spray of Boron at pink bud stage.",  "products": ["Urea", "MOP", "Boron", "Calcium"]},
    "orange":      {"npk": "80:40:80",  "tip": "Split N into 3 doses. Micronutrients (Zinc, Iron, Manganese) essential. Use acid-forming fertilizers.", "products": ["Urea", "MOP", "Zinc Sulphate", "FeSO4"]},
    "papaya":      {"npk": "100:100:150","tip": "Apply monthly in splits. High K requirement for fruit quality. Add Magnesium if leaves yellow.",         "products": ["Urea", "SSP", "MOP"]},
    "coconut":     {"npk": "100:40:140","tip": "Apply 4 times per year. High K demand. Use green manure as organic supplement.",                          "products": ["Urea", "SSP", "MOP", "Borax"]},
    "cotton":      {"npk": "100:50:50", "tip": "Apply N in 3 splits. Avoid excess N (causes vegetative growth). Use MOP for boll development.",          "products": ["Urea", "DAP", "MOP", "Zinc"]},
    "jute":        {"npk": "60:30:30",  "tip": "Nitrogen is key for fibre yield. Apply in 2 splits. Phosphorus improves root development.",              "products": ["Urea", "SSP", "MOP"]},
    "coffee":      {"npk": "60:30:60",  "tip": "Apply N in 2 splits (May & Sep). K improves bean quality. Use organic manure to maintain soil health.",  "products": ["Urea", "MOP", "Bone Meal"]},
}

# ── Crop Rotation Database ────────────────────────────────
# Scientifically recommended next-season crops for soil health
ROTATION_DB = {
    "rice":        {"next": ["Lentil", "Chickpea", "Mustard"],   "reason": "Legumes fix nitrogen depleted by rice."},
    "maize":       {"next": ["Soybean", "Chickpea", "Wheat"],    "reason": "Legumes restore N; wheat breaks pest cycles."},
    "chickpea":    {"next": ["Wheat", "Barley", "Mustard"],      "reason": "Cereal crops benefit from legume-fixed nitrogen."},
    "kidneybeans": {"next": ["Maize", "Cotton", "Wheat"],        "reason": "High-N benefit after legume residue breakdown."},
    "pigeonpeas":  {"next": ["Rice", "Sorghum", "Maize"],        "reason": "Cereals make use of the N enriched soil."},
    "mothbeans":   {"next": ["Wheat", "Mustard", "Barley"],      "reason": "Quick-maturing rabi crops suit the dry soil."},
    "mungbean":    {"next": ["Wheat", "Maize", "Sorghum"],       "reason": "Short duration allows double-cropping with wheat."},
    "blackgram":   {"next": ["Rice", "Maize", "Wheat"],          "reason": "Cereals benefit greatly from blackgram residue."},
    "lentil":      {"next": ["Wheat", "Mustard", "Barley"],      "reason": "Classic rabi rotation for North India plains."},
    "pomegranate": {"next": ["Cover Crop (Cowpea)", "Groundnut"],"reason": "Legume cover crops restore organic matter."},
    "banana":      {"next": ["Legumes", "Ginger", "Turmeric"],   "reason": "Spices and legumes suit post-banana soil."},
    "mango":       {"next": ["Cover Crop (Cowpea)", "Vegetables"],"reason": "Intercrops sustain income between seasons."},
    "grapes":      {"next": ["Garlic", "Onion", "Mustard"],      "reason": "Alliums help control soil-borne diseases."},
    "watermelon":  {"next": ["Maize", "Cowpea", "Beans"],        "reason": "Legumes recover N after heavy watermelon feeding."},
    "muskmelon":   {"next": ["Maize", "Cowpea", "Vegetables"],   "reason": "Intercrop with legumes to restore nutrients."},
    "apple":       {"next": ["Cover Crop (Clover)", "Vegetables"],"reason": "Perennial; interplant clover to fix N."},
    "orange":      {"next": ["Cover Crop (Cowpea)", "Vegetables"],"reason": "Leguminous cover crops restore citrus orchards."},
    "papaya":      {"next": ["Legumes", "Maize", "Turmeric"],    "reason": "Short-cycle crops between papaya rotations."},
    "coconut":     {"next": ["Banana", "Pineapple", "Cocoa"],    "reason": "Perennial intercropping maximises land use."},
    "cotton":      {"next": ["Wheat", "Chickpea", "Linseed"],    "reason": "Rabi legumes fix N and break cotton pest cycle."},
    "jute":        {"next": ["Rice", "Mustard", "Lentil"],       "reason": "Rice benefits from improved jute soil structure."},
    "coffee":      {"next": ["Pepper", "Cardamom", "Cover Crop"],"reason": "Spice intercrops increase farm income."},
}


def get_fertilizer_tip(crop: str) -> dict:
    """
    Return fertilizer recommendation for the given crop.
    Args:
        crop: lowercase crop name (e.g. 'rice')
    Returns:
        dict with keys: npk, tip, products
    """
    return FERTILIZER_DB.get(crop, {
        "npk": "60:30:30",
        "tip": "Apply a balanced NPK fertilizer as per local agronomist advice.",
        "products": ["NPK Complex"]
    })


def get_soil_health_tip(ph: float, n: float, p: float, k: float) -> dict:
    """
    Diagnose soil health based on pH and NPK levels.
    Implements a strict scoring system and generates agricultural insights.
    """
    problems = []
    suggestions = []
    score = 0

    # Nitrogen diagnosis
    if 20 <= n <= 140:
        score += 2
    elif n < 20:
        problems.append(f"Nitrogen LOW ({n}): Plants may show yellow leaves and stunted growth.")
        suggestions.append("Apply Urea or incorporate nitrogen-rich green manure.")
    else:  # n > 140
        score -= 1
        problems.append(f"Nitrogen HIGH ({n}): Excess nitrogen leads to excessive leaf growth but poor fruiting. May burn roots and reduce crop yield.")
        suggestions.append("Reduce urea/nitrogen fertilizer usage immediately.")

    # Phosphorus diagnosis
    if 10 <= p <= 145:
        score += 2
    elif p < 10:
        problems.append(f"Phosphorus LOW ({p}): Weak root development and delayed maturity.")
        suggestions.append("Apply SSP (Single Super Phosphate) or DAP fertilizer.")
    else:  # p > 145
        score -= 1
        problems.append(f"Phosphorus HIGH ({p}): Blocks micronutrient absorption like zinc and iron.")
        suggestions.append("Limit phosphorus applications to prevent water pollution and nutrient lockup.")

    # Potassium diagnosis
    if 20 <= k <= 205:
        score += 2
    elif k < 20:
        problems.append(f"Potassium LOW ({k}): Weak plant resistance to disease and drought.")
        suggestions.append("Apply MOP (Muriate of Potash) fertilizer to boost immunity.")
    else:  # k > 205
        score -= 1
        problems.append(f"Potassium HIGH ({k}): May imbalance magnesium and calcium uptake.")
        suggestions.append("Reduce potassium inputs and monitor soil magnesium levels.")

    # pH diagnosis
    if 6.0 <= ph <= 7.5:
        score += 2
    elif ph < 6.0:
        problems.append(f"pH ACIDIC ({ph}): Nutrient availability decreases, especially phosphorus.")
        suggestions.append("Apply agricultural lime (calcium carbonate) to neutralize acidity.")
    else:  # ph > 7.5
        score -= 1
        problems.append(f"pH ALKALINE ({ph}): Causes micronutrient deficiencies (iron, zinc).")
        suggestions.append("Add organic compost, elemental sulfur, or gypsum to lower pH.")

    # Overall classification
    if score >= 6:
        status, color = "Excellent", "green"
        if not problems:
            problems.append("No critical issues detected. Nutrients are well-balanced.")
        if not suggestions:
            suggestions.append("Maintain current soil practices and add regular organic compost.")
    elif 3 <= score <= 5:
        status, color = "Moderate", "amber"
    else:
        status, color = "Poor", "red"

    return {
        "status": status, 
        "color": color, 
        "score": score,
        "problems": problems,
        "suggestions": suggestions
    }


def get_rotation_suggestion(crop: str) -> dict:
    """
    Return next-season crop rotation advice.
    Args:
        crop: lowercase crop name
    Returns:
        dict with keys: next (list), reason (str)
    """
    return ROTATION_DB.get(crop, {
        "next": ["Legumes", "Green Manure"],
        "reason": "Rotating with legumes is generally recommended to restore soil nitrogen."
    })
