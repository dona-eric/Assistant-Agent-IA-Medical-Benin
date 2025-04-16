from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from src.agent.agent import MedicalAgent

router = APIRouter()
agent = MedicalAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    history: List[Dict]

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await agent.chat(request.message)
        return ChatResponse(
            response=response,
            history=agent.get_conversation_history()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_conversation():
    agent.reset_conversation()
    return {"message": "Conversation réinitialisée"}

@router.get("/history")
async def get_history():
    return {"history": agent.get_conversation_history()} 