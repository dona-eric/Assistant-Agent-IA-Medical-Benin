from fastapi import APIRouter, Depends
from src.config.config import Config
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_appointments():
    return {
        "appointments": [
            {
                "id": 1,
                "patient_id": 1,
                "doctor_id": 1,
                "date": datetime.now().isoformat(),
                "status": "scheduled"
            }
        ]
    }

@router.post("/")
async def create_appointment():
    return {
        "id": 1,
        "patient_id": 1,
        "doctor_id": 1,
        "date": datetime.now().isoformat(),
        "status": "scheduled"
    } 