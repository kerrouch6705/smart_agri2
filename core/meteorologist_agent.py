"""Analyse meteorological conditions for the irrigation workflow."""

from typing import Any


def analyser_meteo(weather_data: dict[str, float]) -> dict[str, Any]:
    """Analyse next-day weather data and its impact on water needs."""
    required_fields = {
        "Temperature_C",
        "Humidity",
        "Rainfall_mm",
        "Wind_Speed_kmh",
    }
    missing_fields = required_fields.difference(weather_data)
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Données météo manquantes : {missing}")

    temperature = weather_data["Temperature_C"]
    humidity = weather_data["Humidity"]
    rainfall = weather_data["Rainfall_mm"]
    wind_speed = weather_data["Wind_Speed_kmh"]

    if rainfall >= 10:
        rainfall_analysis = "Des précipitations importantes sont prévues."
        irrigation_impact = "La pluie peut réduire ou supprimer le besoin d'irrigation."
    elif rainfall > 0:
        rainfall_analysis = "De faibles précipitations sont prévues."
        irrigation_impact = "Les précipitations peuvent réduire légèrement le besoin d'irrigation."
    else:
        rainfall_analysis = "Aucune précipitation n'est prévue."
        irrigation_impact = "L'absence de pluie augmente le besoin potentiel d'irrigation."

    if temperature >= 35:
        temperature_analysis = "La température est très élevée."
    elif temperature >= 28:
        temperature_analysis = "La température est élevée."
    else:
        temperature_analysis = "La température reste modérée."

    if humidity < 40:
        humidity_analysis = "L'humidité de l'air est faible."
    elif humidity <= 70:
        humidity_analysis = "L'humidité de l'air est modérée."
    else:
        humidity_analysis = "L'humidité de l'air est élevée."

    if wind_speed >= 25:
        wind_analysis = "Le vent est fort et peut accélérer l'évaporation."
    elif wind_speed >= 15:
        wind_analysis = "Le vent est modéré."
    else:
        wind_analysis = "Le vent est faible."

    stress_factors = []
    if temperature >= 28:
        stress_factors.append("température élevée")
    if humidity < 40:
        stress_factors.append("humidité de l'air faible")
    if rainfall == 0:
        stress_factors.append("absence de pluie")
    if wind_speed >= 25:
        stress_factors.append("vent fort")

    if stress_factors:
        overall_assessment = (
            "Les conditions météorologiques peuvent augmenter les pertes d'eau : "
            + ", ".join(stress_factors)
            + "."
        )
    else:
        overall_assessment = "Les conditions météorologiques ne montrent pas de risque élevé de perte d'eau."

    return {
        "temperature_analysis": temperature_analysis,
        "humidity_analysis": humidity_analysis,
        "rainfall_analysis": rainfall_analysis,
        "wind_analysis": wind_analysis,
        "irrigation_impact": irrigation_impact,
        "overall_assessment": overall_assessment,
    }