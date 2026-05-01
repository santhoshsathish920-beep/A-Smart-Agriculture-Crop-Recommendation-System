"""
=============================================================
 weather.py  —  OpenWeatherMap API Integration
=============================================================
 Fetches real-time temperature & humidity for a given city.
 Falls back gracefully if API key is missing/invalid.

 Free API: https://openweathermap.org/api
   - Sign up for free
   - Paste key in config.py  (OPENWEATHER_API_KEY)
=============================================================
"""

import requests
from config import OPENWEATHER_API_KEY

# OpenWeatherMap base URL (current weather, metric units)
OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city: str) -> dict:
    """
    Fetch current weather for the given city name.

    Args:
        city: City name string (e.g. 'Chennai', 'Delhi')

    Returns:
        On success:
            {
              "success": True,
              "city": str, "country": str,
              "temperature": float (°C),
              "humidity": float (%),
              "description": str,
              "icon_url": str
            }
        On failure:
            {
              "success": False,
              "error": str
            }
    """

    # Guard: no key provided
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return {
            "success": False,
            "error": "OpenWeatherMap API key not configured. "
                     "Add your key to config.py or set OPENWEATHER_API_KEY env variable."
        }

    params = {
        "q":     city.strip(),
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",   # Celsius
    }

    try:
        resp = requests.get(OWM_URL, params=params, timeout=5)

        # City not found
        if resp.status_code == 404:
            return {"success": False, "error": f"City '{city}' not found. Check spelling."}

        # Invalid API key
        if resp.status_code == 401:
            return {"success": False, "error": "Invalid API key. Check config.py."}

        # Other HTTP errors
        resp.raise_for_status()

        data = resp.json()

        # Extract required fields
        temperature = round(data["main"]["temp"], 1)
        humidity    = round(data["main"]["humidity"], 1)
        description = data["weather"][0]["description"].title()
        icon_code   = data["weather"][0]["icon"]
        icon_url    = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        city_name   = data["name"]
        country     = data["sys"]["country"]

        return {
            "success":     True,
            "city":        city_name,
            "country":     country,
            "temperature": temperature,
            "humidity":    humidity,
            "description": description,
            "icon_url":    icon_url,
        }

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No internet connection."}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Weather service timed out. Try again."}
    except Exception as exc:
        return {"success": False, "error": f"Unexpected error: {exc}"}
