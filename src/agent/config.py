from pydantic import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AgentConfig(BaseSettings):
    # Configuration de l'API Mistral
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-medium")
    
    # Configuration du système
    SYSTEM_PROMPT: str = """Tu es un assistant médical IA spécialisé dans le diagnostic et les conseils médicaux.
    Tu dois :
    1. Écouter attentivement les symptômes décrits
    2. Poser des questions pertinentes pour affiner le diagnostic
    3. Proposer des diagnostics possibles
    4. Donner des conseils médicaux appropriés
    5. Recommander de consulter un médecin si nécessaire
    
    Important :
    - Ne jamais donner de diagnostic définitif sans consultation médicale
    - Toujours recommander de consulter un médecin en cas de symptômes graves
    - Rester professionnel et empathique
    - Adapter tes réponses au contexte médical béninois"""
    
    # Paramètres de génération
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    
    # Historique des conversations
    MAX_HISTORY: int = 10
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instance de configuration
config = AgentConfig() 