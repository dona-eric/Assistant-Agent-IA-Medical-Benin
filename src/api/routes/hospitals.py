from fastapi import APIRouter, Depends
from src.config.config import Config

router = APIRouter()

@router.get("/")
async def get_hospitals():
    return {
        "hospitals": [
            {
                "id": 1,
                "name": "Hôpital National",
                "location": "Cotonou",
                "services": ["Urgence", "Consultation", "Hospitalisation"]
            }
        ]
    }

@router.get("/{hospital_id}")
async def get_hospital(hospital_id: int):
    return {
        "id": hospital_id,
        "name": "Hôpital National",
        "location": "Cotonou",
        "services": ["Urgence", "Consultation", "Hospitalisation"]
    } 