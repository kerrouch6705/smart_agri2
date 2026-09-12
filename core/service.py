import os
from typing import Any

import joblib
import pandas as pd

# ==================================================
# CHARGEMENT DU MODÈLE MACHINE LEARNING
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "rf_pipeline.pkl")

REQUIRED_COLUMNS = [
    "Soil_Type",
    "Soil_pH",
    "Soil_Moisture",
    "Temperature_C",
    "Humidity",
    "Rainfall_mm",
    "Wind_Speed_kmh",
    "Crop_Type",
    "Crop_Growth_Stage",
    "Mulching_Used",
    "Region",
]


def load_model() -> Any:
    """Load the trained pipeline from the project models directory."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def predict_next_day_moisture(data: dict[str, Any]) -> float:
    """Predict next-day soil moisture from one farmer input record."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    input_data = pd.DataFrame([{column: data[column] for column in REQUIRED_COLUMNS}])
    prediction = load_model().predict(input_data)[0]
    return float(prediction)
