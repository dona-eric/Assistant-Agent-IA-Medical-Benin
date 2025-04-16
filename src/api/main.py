from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.config.config import Config
from src.api.router import api_router

app = FastAPI(
    title="Assistant IA Médical Bénin",
    description="API pour l'assistant IA médical au Bénin",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sécurité des hôtes
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # À configurer en production
)

# Routes de base
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API de l'Assistant IA Médical Bénin",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",  # À implémenter
            "ai_model": "ready",      # À implémenter
            "cache": "active"         # À implémenter
        }
    }

# Montage du routeur principal
app.include_router(api_router, prefix=Config.API_PREFIX) 