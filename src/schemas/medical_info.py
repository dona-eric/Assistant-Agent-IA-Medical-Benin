from pydantic import BaseModel
from typing import Optional, List
from .base import IDSchema, TimestampSchema

class MedicalInfoBase(BaseModel):
    """Schéma de base pour les informations médicales"""
    title: str
    content: str
    language: str
    category: str

class MedicalInfoCreate(MedicalInfoBase):
    """Schéma pour la création d'information médicale"""
    tags: List[str] = []
    source: Optional[str] = None
    author: Optional[str] = None
    last_reviewed: Optional[str] = None
    related_diseases: List[str] = []
    symptoms: List[str] = []
    treatments: List[str] = []
    audio_content: Optional[str] = None
    video_content: Optional[str] = None
    image_content: List[str] = []

class MedicalInfoUpdate(BaseModel):
    """Schéma pour la mise à jour d'information médicale"""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    author: Optional[str] = None
    last_reviewed: Optional[str] = None
    related_diseases: Optional[List[str]] = None
    symptoms: Optional[List[str]] = None
    treatments: Optional[List[str]] = None
    audio_content: Optional[str] = None
    video_content: Optional[str] = None
    image_content: Optional[List[str]] = None

class MedicalInfoInDB(IDSchema, TimestampSchema, MedicalInfoBase):
    """Schéma pour les données d'information médicale en base"""
    tags: List[str]
    source: Optional[str]
    author: Optional[str]
    last_reviewed: Optional[str]
    related_diseases: List[str]
    symptoms: List[str]
    treatments: List[str]
    audio_content: Optional[str]
    video_content: Optional[str]
    image_content: List[str]

class MedicalInfoResponse(MedicalInfoInDB):
    """Schéma pour la réponse API"""
    pass

class MedicalInfoSearch(BaseModel):
    """Schéma pour la recherche d'informations médicales"""
    query: str
    language: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = 10
    offset: int = 0 