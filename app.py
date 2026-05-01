"""
=============================================================
 AI-Based Smart Agriculture Crop Recommendation System
 app.py  v2  —  Flask Web Application
=============================================================
 Run after training:
     python train_model.py   (only once)
     python app.py
 Open: http://127.0.0.1:5000
=============================================================
"""

from flask import Flask, render_template, request, jsonify
from predictor import predict_top3, get_all_crops
from weather   import fetch_weather
from config    import CROP_INFO, PRICE_UNIT

# ── App Setup ─────────────────────────────────────────────
app = Flask(__name__)


# ─────────────────────────────────────────────────────────
# Route: Home Page
# ─────────────────────────────────────────────────────────
@app.route("/")
def home():
    """
    Render the main input form.
    Passes all_crops list so the UI can display them dynamically.
    """
    all_crops = get_all_crops()
    return render_template("index.html", all_crops=all_crops)


# ─────────────────────────────────────────────────────────
# Route: Form Prediction (POST → result page)
# ─────────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts HTML form submission.
    Validates inputs, runs Top-3 prediction, renders result.html.
    """
    try:
        n           = float(request.form["nitrogen"])
        p           = float(request.form["phosphorus"])
        k           = float(request.form["potassium"])
        temperature = float(request.form["temperature"])
        humidity    = float(request.form["humidity"])
        ph          = float(request.form["ph"])
        rainfall    = float(request.form["rainfall"])
        city        = request.form.get("city", "").strip()
    except (ValueError, KeyError):
        return render_template("index.html",
                               all_crops=get_all_crops(),
                               error="Invalid input. Please enter valid numbers for all fields.")

    # Run ML prediction
    result = predict_top3(n, p, k, temperature, humidity, ph, rainfall)

    # Build input summary dict for display
    result["inputs"] = {
        "Nitrogen (N)":     n,
        "Phosphorus (P)":   p,
        "Potassium (K)":    k,
        "Temperature (C)":  temperature,
        "Humidity (%)":     humidity,
        "pH Value":         ph,
        "Rainfall (mm)":    rainfall,
    }
    result["city"] = city or None

    # Build chart data: labels + prices for profit comparison chart
    result["chart_labels"] = [c["crop"]  for c in result["top3"]]
    result["chart_prices"]  = [c["price"] for c in result["top3"]]
    result["chart_confs"]   = [c["confidence"] for c in result["top3"]]

    return render_template("result.html", result=result)


# ─────────────────────────────────────────────────────────
# API Route: Weather Auto-Fill  (GET /api/weather?city=Chennai)
# ─────────────────────────────────────────────────────────
@app.route("/api/weather")
def api_weather():
    """
    Returns live temperature and humidity for a city.
    Used by the frontend JS to auto-fill the form fields.

    Query params:
        city (str): city name

    Response JSON:
        success=True  → {success, city, country, temperature, humidity, description, icon_url}
        success=False → {success, error}
    """
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"success": False, "error": "Please provide a city name."})

    data = fetch_weather(city)
    return jsonify(data)


# ─────────────────────────────────────────────────────────
# API Route: JSON Prediction  (POST /api/predict)
# ─────────────────────────────────────────────────────────
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """
    REST API endpoint for programmatic access.

    POST body (JSON):
        {"N":90, "P":42, "K":43, "temperature":20.87,
         "humidity":82.0, "ph":6.5, "rainfall":202.9}

    Response (JSON):
        {
          "status": "success",
          "top3": [ {rank, crop, confidence, price, ...}, ... ],
          "soil_health": {...}
        }
    """
    data = request.get_json(force=True)
    try:
        result = predict_top3(
            float(data["N"]),           float(data["P"]),
            float(data["K"]),           float(data["temperature"]),
            float(data["humidity"]),    float(data["ph"]),
            float(data["rainfall"])
        )
        return jsonify({"status": "success", **result})
    except (KeyError, TypeError) as exc:
        return jsonify({"status": "error",
                        "message": f"Missing or invalid field: {exc}"}), 400
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


# ─────────────────────────────────────────────────────────
# Route: Model Charts
# ─────────────────────────────────────────────────────────
@app.route("/charts")
def charts():
    """Display the three training visualisation charts."""
    return render_template("charts.html")


# ─────────────────────────────────────────────────────────
# Route: All Crops Reference Page
# ─────────────────────────────────────────────────────────
@app.route("/crops")
def crops_page():
    """
    Dynamic crops reference page — lists all supported crops
    with price, season and water requirement. Data pulled live
    from config.py CROP_INFO so no hardcoding in HTML.
    """
    # Sort crops by price descending for a nice profitability table
    sorted_crops = sorted(CROP_INFO.items(),
                          key=lambda x: x[1]["price"], reverse=True)
    crops = [{"name": k.title(), "price_unit": PRICE_UNIT, **v}
             for k, v in sorted_crops]
    return render_template("crops.html", crops=crops)


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
