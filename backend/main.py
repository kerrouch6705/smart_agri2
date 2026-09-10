from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from core.service import predict_next_day_moisture
from core.weather_service import get_next_day_weather_for_region


app = FastAPI(title="Smart Agri Irrigation API")


class IrrigationInput(BaseModel):
    Soil_Type: str
    Soil_pH: float
    Soil_Moisture: float
    Crop_Type: str
    Crop_Growth_Stage: str
    Mulching_Used: str
    Region: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: IrrigationInput) -> dict[str, float]:
    try:
        farmer_data = payload.model_dump()
        weather_data = get_next_day_weather_for_region(payload.Region)
        farmer_data.update(weather_data)
        prediction = predict_next_day_moisture(farmer_data)
    except (FileNotFoundError, ValueError, KeyError, OSError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"predicted_soil_moisture": prediction}
