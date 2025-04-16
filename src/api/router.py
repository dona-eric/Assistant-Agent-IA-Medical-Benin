from fastapi import APIRouter
from src.api.routes.auth import router as auth_router
from src.api.routes.hospitals import router as hospitals_router
from src.api.routes.appointments import router as appointments_router
from src.api.routes.medical_info import router as medical_info_router
from src.api.routes.emergency import router as emergency_router
from src.api.routes.user import router as user_router
from src.api.routes.agent import router as agent_router

# Création du routeur principal
api_router = APIRouter()

# Montage des sous-routeurs
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(hospitals_router, prefix="/hospitals", tags=["hospitals"])
api_router.include_router(appointments_router, prefix="/appointments", tags=["appointments"])
api_router.include_router(medical_info_router, prefix="/medical-info", tags=["medical-info"])
api_router.include_router(emergency_router, prefix="/emergency", tags=["emergency"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(agent_router, prefix="/agent", tags=["agent"]) 