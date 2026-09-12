from core.irrigation_rules import construire_recommandation_irrigation


def test_low_predicted_moisture_returns_medium_irrigation() -> None:
    result = construire_recommandation_irrigation(
        predicted_soil_moisture=18.0,
        rainfall_mm=0.0,
        soil_type="Clay",
        crop_growth_stage="Vegetative",
    )

    assert result["irrigation_level"] == "modérée"
    assert result["recommended_water_mm"] == 12.0


def test_significant_rain_stops_irrigation() -> None:
    result = construire_recommandation_irrigation(
        predicted_soil_moisture=10.0,
        rainfall_mm=15.0,
        soil_type="Sandy",
        crop_growth_stage="Flowering",
    )

    assert result["irrigation_level"] == "aucune"
    assert result["recommended_water_mm"] == 0.0