from fastapi import APIRouter, Depends
from src.config.config import Config

router = APIRouter()

@router.get("/symptoms")
async def get_symptoms():
    return {
        "symptoms": [
            {
                "id": 1,
                "name": "Fièvre",
                "description": "Température corporelle élevée",
                "severity": "moderate"
            }
        ]
    }

@router.get("/diseases")
async def get_diseases():
    return {
        "diseases": [
            {
                "id": 1,
                "name": "Paludisme",
                "description": "Maladie transmise par les moustiques",
                "symptoms": ["Fièvre", "Maux de tête", "Fatigue"]
            }
        ]
    } 