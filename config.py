"""
=============================================================
 config.py  —  Central Configuration
=============================================================
 All app-wide constants live here.
 To use live weather:
   Set OPENWEATHER_API_KEY to your free key from:
   https://openweathermap.org/api  (free tier is enough)
=============================================================
"""

import os

# ── OpenWeatherMap API Key ────────────────────────────────
# Priority: environment variable > hardcoded placeholder
OPENWEATHER_API_KEY = os.environ.get(
    "OPENWEATHER_API_KEY",
    "4137e401b907e26d19258307e424689f"          # <-- paste your key here
)

# ── Crop Info Dictionary ──────────────────────────────────
# Keys must match dataset label column (lowercase)
# price = India MSP 2023-24 or realistic market value (₹/quintal)
CROP_INFO = {
    "rice":        {"price": 2183,  "season": "Kharif",  "icon": "🌾",
                    "water": "High",   "duration": "120-150 days"},
    "maize":       {"price": 1962,  "season": "Kharif",  "icon": "🌽",
                    "water": "Medium", "duration": "80-100 days"},
    "chickpea":    {"price": 5440,  "season": "Rabi",    "icon": "🫘",
                    "water": "Low",    "duration": "95-110 days"},
    "kidneybeans": {"price": 7000,  "season": "Kharif",  "icon": "🫘",
                    "water": "Medium", "duration": "100-120 days"},
    "pigeonpeas":  {"price": 7000,  "season": "Kharif",  "icon": "🫘",
                    "water": "Low",    "duration": "150-180 days"},
    "mothbeans":   {"price": 5500,  "season": "Kharif",  "icon": "🫘",
                    "water": "Low",    "duration": "75-90 days"},
    "mungbean":    {"price": 8558,  "season": "Kharif",  "icon": "🫘",
                    "water": "Low",    "duration": "60-75 days"},
    "blackgram":   {"price": 6950,  "season": "Kharif",  "icon": "🫘",
                    "water": "Low",    "duration": "70-80 days"},
    "lentil":      {"price": 6000,  "season": "Rabi",    "icon": "🫘",
                    "water": "Low",    "duration": "110-130 days"},
    "pomegranate": {"price": 8500,  "season": "Annual",  "icon": "🍎",
                    "water": "Low",    "duration": "5-7 months"},
    "banana":      {"price": 3500,  "season": "Annual",  "icon": "🍌",
                    "water": "High",   "duration": "10-12 months"},
    "mango":       {"price": 9000,  "season": "Summer",  "icon": "🥭",
                    "water": "Medium", "duration": "3-5 months"},
    "grapes":      {"price": 7500,  "season": "Annual",  "icon": "🍇",
                    "water": "Medium", "duration": "Annual"},
    "watermelon":  {"price": 1800,  "season": "Summer",  "icon": "🍉",
                    "water": "Medium", "duration": "70-90 days"},
    "muskmelon":   {"price": 2200,  "season": "Summer",  "icon": "🍈",
                    "water": "Medium", "duration": "75-100 days"},
    "apple":       {"price": 12000, "season": "Annual",  "icon": "🍏",
                    "water": "Medium", "duration": "Annual"},
    "orange":      {"price": 4200,  "season": "Winter",  "icon": "🍊",
                    "water": "Medium", "duration": "7-12 months"},
    "papaya":      {"price": 1600,  "season": "Annual",  "icon": "🧡",
                    "water": "Medium", "duration": "9-11 months"},
    "coconut":     {"price": 3200,  "season": "Annual",  "icon": "🥥",
                    "water": "High",   "duration": "Annual"},
    "cotton":      {"price": 6620,  "season": "Kharif",  "icon": "🌸",
                    "water": "Medium", "duration": "150-180 days"},
    "jute":        {"price": 4500,  "season": "Kharif",  "icon": "🌿",
                    "water": "High",   "duration": "100-120 days"},
    "coffee":      {"price": 18000, "season": "Annual",  "icon": "☕",
                    "water": "High",   "duration": "Annual"},
}

# Unit label used in all price displays
PRICE_UNIT = "Rs / quintal"

# Maximum price in dict — used to calculate relative profitability %
MAX_PRICE = max(v["price"] for v in CROP_INFO.values())
