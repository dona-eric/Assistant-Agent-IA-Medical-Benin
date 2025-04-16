from fastapi import APIRouter, Depends
from src.config.config import Config

router = APIRouter()

@router.post("/alert")
async def send_emergency_alert():
    return {
        "status": "alert_sent",
        "message": "Alerte d'urgence envoyée",
        "timestamp": "2024-03-14T12:00:00Z"
    }

@router.get("/nearest-hospitals")
async def get_nearest_hospitals():
    return {
        "hospitals": [
            {
                "id": 1,
                "name": "Hôpital d'Urgence",
                "distance": "2.5 km",
                "estimated_time": "5 minutes"
            }
        ]
    } 