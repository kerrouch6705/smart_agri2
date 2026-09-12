"""Coordinate the deterministic irrigation analysis components."""

import os
from typing import Any

from core.agronomist_agent import analyser_agronomie
from core.groq_workflow import executer_workflow_groq
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

    llm_analysis: dict[str, str] | None = None
    llm_status = "fallback_deterministic"
    llm_error: str | None = None
    if os.getenv("GROQ_API_KEY"):
        try:
            llm_analysis = executer_workflow_groq(
                farmer_data=farmer_data,
                weather_data=weather_data,
                predicted_soil_moisture=predicted_soil_moisture,
                recommendation=recommendation,
            )
            llm_status = "groq_langgraph"
        except Exception as error:
            llm_status = "groq_error_fallback"
            llm_error = f"{type(error).__name__}: {error}"

    result = {
        "predicted_soil_moisture": predicted_soil_moisture,
        "weather_data": weather_data,
        "analyse_meteorologique": meteorological_analysis,
        "analyse_agronomique": agronomic_analysis,
        "recommendation": recommendation,
        "llm_status": llm_status,
    }
    if llm_error:
        result["llm_error"] = llm_error
    if llm_analysis:
        result["analyse_meteorologique_llm"] = llm_analysis["analyse_meteorologique"]
        result["analyse_agronomique_llm"] = llm_analysis["analyse_agronomique"]
    return result