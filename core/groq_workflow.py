"""Groq and LangGraph workflow for irrigation explanations.

The deterministic ML prediction and irrigation rules remain authoritative.
Groq agents only analyse and explain the already computed values.
"""

import os
from typing import Any, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

load_dotenv()


class IrrigationState(TypedDict, total=False):
    farmer_data: dict[str, Any]
    weather_data: dict[str, float]
    predicted_soil_moisture: float
    recommendation: dict[str, Any]
    analyse_meteorologique: str
    analyse_agronomique: str


def _call_groq(system_prompt: str, user_data: dict[str, Any]) -> str:
    """Call Groq only when the API key is configured."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY est absente. Configurez-la avant d'utiliser les agents LLM."
        )

    from langchain_groq import ChatGroq

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=api_key,
    )
    response = model.invoke(
        [
            ("system", system_prompt),
            ("human", str(user_data)),
        ]
    )
    return str(response.content)


def noeud_meteorologue(state: IrrigationState) -> dict[str, str]:
    """Ask Groq to explain the weather impact on irrigation."""
    analysis = _call_groq(
        """Tu es un météorologue agricole. Analyse uniquement les données météo fournies.
Explique leur impact sur les pertes d'eau et le besoin potentiel d'irrigation.
N'invente aucune valeur et réponds en français de façon concise.""",
        state["weather_data"],
    )
    return {"analyse_meteorologique": analysis}


def noeud_agronome(state: IrrigationState) -> dict[str, str]:
    """Ask Groq to explain the agronomic context and existing recommendation."""
    analysis = _call_groq(
        """Tu es un agronome spécialisé en irrigation. Analyse les données de la parcelle,
la prédiction ML et la recommandation calculée par les règles.
Explique la recommandation sans modifier le niveau ni la quantité d'eau fournis.
Réponds en français de façon concise.""",
        {
            "farmer_data": state["farmer_data"],
            "predicted_soil_moisture": state["predicted_soil_moisture"],
            "recommendation": state["recommendation"],
        },
    )
    return {"analyse_agronomique": analysis}


def construire_workflow_groq():
    """Build the LangGraph workflow used by the two Groq agents."""
    workflow = StateGraph(IrrigationState)
    workflow.add_node("meteorologue", noeud_meteorologue)
    workflow.add_node("agronome", noeud_agronome)
    workflow.add_edge(START, "meteorologue")
    workflow.add_edge("meteorologue", "agronome")
    workflow.add_edge("agronome", END)
    return workflow.compile()


def executer_workflow_groq(
    farmer_data: dict[str, Any],
    weather_data: dict[str, float],
    predicted_soil_moisture: float,
    recommendation: dict[str, Any],
) -> dict[str, str]:
    """Run the meteorologist and agronomist nodes in sequence."""
    workflow = construire_workflow_groq()
    result = workflow.invoke(
        {
            "farmer_data": farmer_data,
            "weather_data": weather_data,
            "predicted_soil_moisture": predicted_soil_moisture,
            "recommendation": recommendation,
        }
    )
    return {
        "analyse_meteorologique": result["analyse_meteorologique"],
        "analyse_agronomique": result["analyse_agronomique"],
    }