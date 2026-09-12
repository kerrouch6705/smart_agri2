"""Coordinate the deterministic irrigation analysis components."""

from typing import Any

from core.agronomist_agent import analyser_agronomie
from core.meteorologist_agent import analyser_meteo


def orchestrer_analyse_irrigation(
    farmer_data: dict[str, Any],
    weather_data: dict[str, float],
    predicted_soil_moisture: float,
    recommendation: dict[str, Any],
) -> dict[str, Any]:
    """Combine meteorological and agronomic analyses into one result."""
    meteorological_analysis = analyser_meteo(weather_data)
    agronomic_analysis = analyser_agronomie(
        soil_type=farmer_data["Soil_Type"],
        crop_type=farmer_data["Crop_Type"],
        crop_growth_stage=farmer_data["Crop_Growth_Stage"],
        current_soil_moisture=farmer_data["Soil_Moisture"],
        predicted_soil_moisture=predicted_soil_moisture,
        recommendation=recommendation,
    )

    return {
        "predicted_soil_moisture": predicted_soil_moisture,
        "weather_data": weather_data,
        "analyse_meteorologique": meteorological_analysis,
        "analyse_agronomique": agronomic_analysis,
        "recommendation": recommendation,
    }