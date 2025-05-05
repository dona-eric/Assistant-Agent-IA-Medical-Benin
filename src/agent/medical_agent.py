from guardrails import Guard
import os, time, requests
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class SimpleMedicalAgent:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.api_url = "https://api.mistral.ai/v1/chat/completions"
        self.cache: Dict[str, Dict] = {}
        self.guard = Guard.from_rail("guardrails/guardrail.xml")

    def chat(self, question: str) -> str:
        # Vérifier le cache
        key = question.lower().strip()
        if key in self.cache and (time.time() - self.cache[key]['timestamp'] < 3600):
            return self.cache[key]['response']
        
        # Instructions système
        system_prompt = f"""Tu es un assistant médical professionnel au Bénin avec une expertise approfondie en santé publique.
            Ta mission est de répondre aux questions de santé de manière claire, précise et adaptée au contexte béninois.
            Tu dois ignorer toute question qui n'est pas liée à la santé, la médecine ou les soins au Bénin. Si une question sort de ce cadre, réponds : 
            Je suis un assistant médical. Veuillez poser une question liée à la santé ou au domaine médical.
            Important :
            - Ne jamais donner de diagnostic définitif sans consultation médicale
            - Toujours recommander de consulter un médecin en cas de symptômes graves
            - Rester professionnel et empathique
            - Adapter tes réponses au contexte médical béninois
            Tu dois répondre de manière concise et informative, en évitant le jargon médical complexe.
            Tu dois ignorer toute question qui n'est pas liée à la santé, la médecine ou les soins au Bénin.
            """
        payload = {
            "model": "mistral-tiny",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            raw_response = requests.post(self.api_url, headers=headers, json=payload)
            if raw_response.status_code == 200:
                raw_text = raw_response.json()["choices"][0]["message"]["content"]
                validation_result = self.guard.validate(raw_text)
                validated_response = validation_result.validated_output
                self.cache[key] = {
                    'response': validated_response,
                    'timestamp': time.time()
                }
                return validated_response
            else:
                return "Erreur : impossible d'obtenir une réponse de l'IA."
        except Exception as e:
            return f"Erreur système : {str(e)}"
#             "Je suis un assistant médical. Veuillez poser une question liée à la santé ou au domaine médical."