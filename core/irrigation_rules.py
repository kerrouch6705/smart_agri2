"""Premières recommandations d'irrigation déterministes.

Les seuils proposés sont une première version et doivent être validés à
l'aide de références agronomiques et d'observations sur le terrain avant
une utilisation en production.
"""

from typing import Any


def construire_recommandation_irrigation(
    predicted_soil_moisture: float,
    rainfall_mm: float,
    soil_type: str,
    crop_growth_stage: str,
) -> dict[str, Any]:
    """Convertir les résultats du modèle ML et de la météo en plan d'irrigation."""
    if predicted_soil_moisture < 0:
        raise ValueError("Predicted soil moisture cannot be negative")
    if rainfall_mm < 0:
        raise ValueError("Rainfall cannot be negative")

    if rainfall_mm >= 10:
        return {
            "irrigation_level": "aucune",
            "recommended_water_mm": 0.0,
            "timing": "Pas d'irrigation pour le moment",
            "reason": "Des précipitations importantes sont prévues.",
        }

    if predicted_soil_moisture < 15:
        level = "forte"
        water_mm = 20.0
        reason = "L'humidité du sol prévue est très faible."
    elif predicted_soil_moisture < 25:
        level = "modérée"
        water_mm = 12.0
        reason = "L'humidité du sol prévue est faible."
    elif predicted_soil_moisture < 35:
        level = "faible"
        water_mm = 6.0
        reason = "L'humidité du sol prévue est moyenne."
    else:
        level = "aucune"
        water_mm = 0.0
        reason = "L'humidité du sol prévue est suffisante."

    if soil_type == "Sandy" and level in {"modérée", "forte"}:
        water_mm += 3.0
        reason += " Le sol sableux perd rapidement son eau."
    elif soil_type == "Clay" and level == "forte":
        water_mm -= 3.0
        reason += " Le sol argileux retient l'eau plus longtemps."

    if crop_growth_stage == "Flowering" and level != "aucune":
        reason += " La phase de floraison est sensible au manque d'eau."

    return {
        "irrigation_level": level,
        "recommended_water_mm": water_mm,
        "timing": "Tôt le matin",
        "reason": reason,
    }