from fastapi import APIRouter, Depends
from src.config.config import Config

router = APIRouter()

@router.get("/profile")
async def get_user_profile():
    return {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com",
        "role": "patient",
        "medical_history": []
    }

@router.put("/profile")
async def update_user_profile():
    return {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com",
        "role": "patient",
        "medical_history": []
    } 