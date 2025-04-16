from pydantic import BaseModel, constr
from typing import Optional, List, Dict
from .base import IDSchema, TimestampSchema

class HospitalBase(BaseModel):
    """Schéma de base pour les hôpitaux"""
    name: str
    address: str
    latitude: float
    longitude: float
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    type: str  # public, private, community
    level: Optional[str] = None  # primary, secondary, tertiary

class HospitalCreate(HospitalBase):
    """Schéma pour la création d'hôpital"""
    specialties: List[str] = []
    services: List[str] = []
    working_hours: Dict = {}
    emergency_services: bool = False
    description: Optional[str] = None
    facilities: List[str] = []
    insurance_accepted: List[str] = []
    languages_spoken: List[str] = []

class HospitalUpdate(BaseModel):
    """Schéma pour la mise à jour d'hôpital"""
    name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    working_hours: Optional[Dict] = None
    description: Optional[str] = None
    facilities: Optional[List[str]] = None
    insurance_accepted: Optional[List[str]] = None
    languages_spoken: Optional[List[str]] = None

class HospitalInDB(IDSchema, TimestampSchema, HospitalBase):
    """Schéma pour les données d'hôpital en base"""
    specialties: List[str]
    services: List[str]
    working_hours: Dict
    emergency_services: bool
    description: Optional[str]
    facilities: List[str]
    insurance_accepted: List[str]
    languages_spoken: List[str]

class HospitalResponse(HospitalInDB):
    """Schéma pour la réponse API"""
    pass

class HospitalSearch(BaseModel):
    """Schéma pour la recherche d'hôpitaux"""
    latitude: float
    longitude: float
    radius: float = 10.0  # en kilomètres
    specialties: Optional[List[str]] = None
    emergency_services: Optional[bool] = None
    type: Optional[str] = None 