import os
from dotenv import load_dotenv
import requests
import json
from typing import Dict, Optional
import time

# Charger les variables d'environnement
load_dotenv()

class MedicalAgent:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.cache: Dict[str, Dict] = {}
        
    def get_response(self, question: str) -> str:
        # Vérifier le cache
        cache_key = question.lower().strip()
        if cache_key in self.cache:
            cached_response = self.cache[cache_key]
            if time.time() - cached_response['timestamp'] < 3600:  # Cache valide pendant 1 heure
                return cached_response['response']
        
        # Préparer le prompt
        prompt = f"""Tu es un assistant médical professionnel au Bénin avec une expertise approfondie en santé publique.
Ta mission est de répondre aux questions de santé de manière claire, précise et adaptée au contexte béninois.

Question: {question}

Pour les questions sur les maladies :
- Décris les symptômes principaux
- Explique les causes possibles
- Donne des conseils de prévention adaptés au contexte béninois
- Recommande quand consulter un médecin
- Mentionne les centres de santé appropriés au Bénin

Pour les questions sur les traitements :
- Explique les options disponibles au Bénin
- Mentionne les précautions à prendre
- Indique les centres spécialisés au Bénin

Réponds de manière professionnelle et bien structurée."""
        
        # Obtenir la réponse de l'API
        response = self._query_api(prompt)
        
        if response:
            # Mettre en cache
            self.cache[cache_key] = {
                'response': response,
                'timestamp': time.time()
            }
            return response
        else:
            return """
            Je suis désolé, je ne peux pas répondre à cette question pour le moment.
            Veuillez réessayer plus tard ou consulter un professionnel de santé.
            """
    
    def _query_api(self, prompt: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json={
                    "model": "mistral-tiny",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Tu es un assistant médical professionnel au Bénin avec une expertise approfondie en santé publique."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"Erreur API: {response.status_code}")
                print(f"Détails: {response.text}")
                return None
        except Exception as e:
            print(f"Erreur de connexion: {str(e)}")
            return None

# Test de l'agent
if __name__ == "__main__":
    agent = MedicalAgent()
    test_question = "Quels sont les symptômes du paludisme et comment le prévenir au Bénin ?"
    response = agent.get_response(test_question)
    print("\nQuestion:", test_question)
    print("\nRéponse:", response) 