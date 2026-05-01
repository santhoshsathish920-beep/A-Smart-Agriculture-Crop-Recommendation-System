# 🌾 AI-Based Smart Agriculture Crop Recommendation System

A machine-learning web application that predicts the best crop for a given region
using soil nutrients and environmental data, built with **Python + Flask + Scikit-learn**.

---

## 📁 Project Structure

```
Agri Recommendation/
│
├── app.py                    # Flask web application (main entry point)
├── train_model.py            # ML model training script (run once)
├── Crop_Recommendation.csv   # Dataset (22 crops, 7 features)
├── requirements.txt          # Python dependencies
│
├── model/                    # Auto-created after training
│   ├── crop_model.pkl        # Trained RandomForestClassifier
│   └── label_encoder.pkl     # Label encoder for crop names
│
├── templates/
│   ├── index.html            # Home page with input form
│   ├── result.html           # Prediction result page
│   └── charts.html           # Data visualisation page
│
└── static/
    ├── style.css             # Global dark-theme stylesheet
    └── charts/               # Auto-created after training
        ├── feature_importance.png
        ├── crop_distribution.png
        └── confusion_matrix.png
```

---

## 🚀 How to Run

### Step 1 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Train the model (run once)
```bash
python train_model.py
```
This will:
- Load the dataset
- Train a RandomForestClassifier
- Evaluate and print accuracy
- Save the model to `model/`
- Save 3 charts to `static/charts/`

### Step 3 – Start the web application
```bash
python app.py
```

### Step 4 – Open in your browser
```
http://127.0.0.1:5000
```

---

## 🌐 Pages

| URL          | Description                          |
|--------------|--------------------------------------|
| `/`          | Home page with 7-parameter input form |
| `/predict`   | POST route — returns prediction result |
| `/charts`    | Data visualisation (3 charts)         |
| `/api/predict` | JSON API endpoint for programmatic use |

---

## 📊 Input Parameters

| Parameter       | Unit   | Typical Range |
|-----------------|--------|---------------|
| Nitrogen (N)    | mg/kg  | 0 – 140       |
| Phosphorus (P)  | mg/kg  | 5 – 145       |
| Potassium (K)   | mg/kg  | 5 – 205       |
| Temperature     | °C     | 8 – 44        |
| Humidity        | %      | 14 – 100      |
| pH Value        | pH     | 3.5 – 9.0     |
| Rainfall        | mm     | 20 – 300      |

---

## 🧪 Example Input & Output

**Input:**
```
N=90, P=42, K=43, Temperature=20.87, Humidity=82, pH=6.5, Rainfall=202.9
```

**Output:**
```
Predicted Crop : Rice 🌾
Confidence     : 98.5%
Market Price   : ₹2,300 / quintal
Growing Season : Kharif
Top 3 Profitable Crops: Coffee ☕, Apple 🍏, Mango 🥭
```

---

## 🤖 Machine Learning Details

- **Algorithm**: RandomForestClassifier (100 trees, max depth 10)
- **Train/Test Split**: 80% / 20%
- **Accuracy**: ~100% on mock dataset
- **Features**: 7 (N, P, K, temperature, humidity, ph, rainfall)
- **Classes**: 22 crops

---

## 💰 Supported Crops & Prices (₹/quintal)

| Crop        | Price  | Season  |
|-------------|--------|---------|
| Coffee      | 18,000 | Annual  |
| Apple       | 12,000 | Annual  |
| Mango       | 9,000  | Summer  |
| Pomegranate | 8,500  | Annual  |
| Mungbean    | 7,755  | Kharif  |
| Kidneybeans | 7,000  | Kharif  |
| ... and 16 more |    |         |

---

## 🔌 JSON API Usage

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":20.87,"humidity":82,"ph":6.5,"rainfall":202.9}'
```

Response:
```json
{
  "status": "success",
  "result": {
    "crop": "Rice",
    "confidence": 98.5,
    "price": 2300,
    "unit": "₹ / quintal",
    "season": "Kharif",
    "icon": "🌾",
    "top3": [...]
  }
}
```

---

*Built for educational/demonstration purposes. Always consult a local agricultural expert.*
