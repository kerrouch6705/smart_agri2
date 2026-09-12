from core.agronomist_agent import analyser_agronomie


def test_analyser_agronomie_explains_low_moisture() -> None:
    result = analyser_agronomie(
        soil_type="Clay",
        crop_type="Wheat",
        crop_growth_stage="Vegetative",
        current_soil_moisture=18.0,
        predicted_soil_moisture=9.8,
        recommendation={
            "irrigation_level": "forte",
            "recommended_water_mm": 17.0,
        },
    )

    assert "argileux" in result["soil_analysis"]
    assert "diminue fortement" in result["moisture_analysis"]
    assert "Wheat" in result["crop_analysis"]