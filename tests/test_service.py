from core.service import predict_next_day_moisture


def test_predict_next_day_moisture_returns_number() -> None:
    data = {
        "Soil_Type": "Clay",
        "Soil_pH": 6.5,
        "Soil_Moisture": 18.0,
        "Temperature_C": 32.0,
        "Humidity": 35.0,
        "Rainfall_mm": 2.0,
        "Wind_Speed_kmh": 15.0,
        "Crop_Type": "Wheat",
        "Crop_Growth_Stage": "Vegetative",
        "Mulching_Used": "No",
        "Region": "North",
    }

    prediction = predict_next_day_moisture(data)

    assert isinstance(prediction, float)
