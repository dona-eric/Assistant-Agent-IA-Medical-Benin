import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    # Configuration de la base de données
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/medical_assistant')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/medical_assistant')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Configuration de l'API
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-here')
    
    # Configuration des services externes
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    
    # Configuration du modèle IA
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    MODEL_NAME = os.getenv('MODEL_NAME', 'llama2')
    
    # Configuration des langues supportées
    SUPPORTED_LANGUAGES = ['fr', 'fon', 'yo', 'ba']
    DEFAULT_LANGUAGE = 'fr'
    
    # Configuration du cache
    CACHE_TIMEOUT = 3600  # 1 heure en secondes
    
    # Configuration de la sécurité
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    RATE_LIMIT = "100/minute"
    
    # Configuration du mode hors-ligne
    OFFLINE_MODE_ENABLED = os.getenv('OFFLINE_MODE_ENABLED', 'True').lower() == 'true'
    OFFLINE_SYNC_INTERVAL = 300  # 5 minutes en secondes 