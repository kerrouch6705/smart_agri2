from core.orchestrator import orchestrer_analyse_irrigation


def test_orchestrator_combines_both_agents() -> None:
    result = orchestrer_analyse_irrigation(
        farmer_data={
            "Soil_Type": "Clay",
            "Soil_Moisture": 18.0,
            "Crop_Type": "Wheat",
            "Crop_Growth_Stage": "Vegetative",
        },
        weather_data={
            "Temperature_C": 32.0,
            "Humidity": 35.0,
            "Rainfall_mm": 0.0,
            "Wind_Speed_kmh": 15.0,
        },
        predicted_soil_moisture=9.8,
        recommendation={
            "irrigation_level": "forte",
            "recommended_water_mm": 17.0,
        },
    )

    assert "analyse_meteorologique" in result
    assert "analyse_agronomique" in result
    assert result["recommendation"]["irrigation_level"] == "forte"