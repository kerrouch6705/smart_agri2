from core.meteorologist_agent import analyser_meteo


def test_analyser_meteo_detects_dry_conditions() -> None:
    result = analyser_meteo(
        {
            "Temperature_C": 32.0,
            "Humidity": 35.0,
            "Rainfall_mm": 0.0,
            "Wind_Speed_kmh": 15.0,
        }
    )

    assert "température élevée" in result["overall_assessment"]
    assert "absence de pluie" in result["overall_assessment"]
    assert "augmente" in result["irrigation_impact"]