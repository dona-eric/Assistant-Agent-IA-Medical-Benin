from typing import List, Dict, Optional
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .config import config
import json

class MedicalAgent:
    def __init__(self):
        self.client = MistralClient(api_key=config.MISTRAL_API_KEY)
        self.conversation_history: List[Dict] = []
        self.system_message = ChatMessage(
            role="system",
            content=config.SYSTEM_PROMPT
        )
    
    def _format_message(self, role: str, content: str) -> ChatMessage:
        """Formate un message pour l'API Mistral"""
        return ChatMessage(role=role, content=content)
    
    def _update_history(self, role: str, content: str):
        """Met à jour l'historique de la conversation"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Garder uniquement les N derniers messages
        if len(self.conversation_history) > config.MAX_HISTORY:
            self.conversation_history = self.conversation_history[-config.MAX_HISTORY:]
    
    async def chat(self, user_message: str) -> str:
        """Gère une conversation avec l'utilisateur"""
        try:
            # Ajouter le message de l'utilisateur à l'historique
            self._update_history("user", user_message)
            
            # Préparer les messages pour l'API
            messages = [self.system_message]
            for msg in self.conversation_history:
                messages.append(self._format_message(msg["role"], msg["content"]))
            
            # Appeler l'API Mistral
            response = self.client.chat(
                model=config.MISTRAL_MODEL,
                messages=messages,
                max_tokens=config.MAX_TOKENS,
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P
            )
            
            # Extraire la réponse
            assistant_message = response.choices[0].message.content
            
            # Ajouter la réponse à l'historique
            self._update_history("assistant", assistant_message)
            
            return assistant_message
            
        except Exception as e:
            return f"Désolé, une erreur s'est produite : {str(e)}"
    
    def reset_conversation(self):
        """Réinitialise l'historique de la conversation"""
        self.conversation_history = []
    
    def get_conversation_history(self) -> List[Dict]:
        """Retourne l'historique de la conversation"""
        return self.conversation_history 