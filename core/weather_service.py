import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


# ==================================================
# RÉGIONS SUPPORTÉES (pour récupérer la météo automatiquement)
# ==================================================
REGION_COORDINATES = {
    "Souss-Massa": {"latitude": 30.4278, "longitude": -9.5981},
    "Agadir": {"latitude": 30.4278, "longitude": -9.5981},
    "Taroudant": {"latitude": 30.4703, "longitude": -8.8769},
    "Marrakech": {"latitude": 31.6295, "longitude": -7.9811},
    "Casablanca": {"latitude": 33.5731, "longitude": -7.5898},
}

# ==================================================
# MÉTÉO (OPEN-METEO)
# ==================================================
def get_next_day_weather_for_region(region: str) -> dict[str, float]:
    """Fetch next-day weather using the coordinates configured for a region."""
    coordinates = REGION_COORDINATES.get(region)
    if coordinates is None:
        supported_regions = ", ".join(REGION_COORDINATES)
        raise ValueError(
            f"Unsupported region '{region}'. Supported regions: {supported_regions}"
        )

    params = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max",
        "forecast_days": 2,
        "timezone": "auto",
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    daily = data["daily"]
    return {
        "Temperature_C": float(daily["temperature_2m_mean"][1]),
        "Humidity": float(daily["relative_humidity_2m_mean"][1]),
        "Rainfall_mm": float(daily["precipitation_sum"][1]),
        "Wind_Speed_kmh": float(daily["wind_speed_10m_max"][1]),
    }
