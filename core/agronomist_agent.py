"""Analyse agronomic conditions for the irrigation workflow."""

from typing import Any


def analyser_agronomie(
    soil_type: str,
    crop_type: str,
    crop_growth_stage: str,
    current_soil_moisture: float,
    predicted_soil_moisture: float,
    recommendation: dict[str, Any],
) -> dict[str, Any]:
    """Analyse soil and crop conditions around the rule-based recommendation."""
    if current_soil_moisture < 0 or predicted_soil_moisture < 0:
        raise ValueError("L'humidité du sol ne peut pas être négative.")

    if soil_type == "Sandy":
        soil_analysis = "Le sol sableux se draine rapidement et demande des apports plus fréquents."
    elif soil_type == "Clay":
        soil_analysis = "Le sol argileux retient davantage l'eau et nécessite une irrigation contrôlée."
    elif soil_type == "Silt":
        soil_analysis = "Le sol limoneux possède une capacité moyenne de rétention d'eau."
    else:
        soil_analysis = "Le type de sol doit être surveillé pour ajuster précisément l'irrigation."

    sensitive_stages = {"Sowing", "Vegetative", "Flowering"}
    if crop_growth_stage == "Flowering":
        stage_analysis = "La floraison est une phase sensible au déficit hydrique."
    elif crop_growth_stage in sensitive_stages:
        stage_analysis = "La culture est dans une phase où un suivi régulier de l'humidité est recommandé."
    else:
        stage_analysis = "La culture est dans une phase moins sensible, mais l'humidité doit rester surveillée."

    moisture_change = predicted_soil_moisture - current_soil_moisture
    if moisture_change < -5:
        moisture_analysis = "L'humidité prévue diminue fortement par rapport à l'humidité actuelle."
    elif moisture_change < 0:
        moisture_analysis = "L'humidité prévue diminue légèrement par rapport à l'humidité actuelle."
    else:
        moisture_analysis = "L'humidité prévue reste stable ou augmente."

    level = recommendation["irrigation_level"]
    conclusion = (
        f"Pour la culture de {crop_type}, une irrigation {level} est recommandée "
        f"avec environ {recommendation['recommended_water_mm']} mm d'eau."
    )

    return {
        "soil_analysis": soil_analysis,
        "crop_analysis": f"Culture concernée : {crop_type}.",
        "growth_stage_analysis": stage_analysis,
        "moisture_analysis": moisture_analysis,
        "agronomic_conclusion": conclusion,
    }