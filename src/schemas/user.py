from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Dict, List
from .base import IDSchema, TimestampSchema

class UserBase(BaseModel):
    """Schéma de base pour les utilisateurs"""
    phone_number: constr(min_length=8, max_length=20)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    language_preference: str = "fr"

class UserCreate(UserBase):
    """Schéma pour la création d'utilisateur"""
    password: constr(min_length=8)

class UserUpdate(BaseModel):
    """Schéma pour la mise à jour d'utilisateur"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    language_preference: Optional[str] = None
    preferences: Optional[Dict] = None

class UserInDB(IDSchema, TimestampSchema, UserBase):
    """Schéma pour les données utilisateur en base"""
    is_active: bool
    is_verified: bool
    preferences: Dict

class UserResponse(UserInDB):
    """Schéma pour la réponse API"""
    pass

class UserLogin(BaseModel):
    """Schéma pour la connexion"""
    phone_number: constr(min_length=8, max_length=20)
    password: str

class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schéma pour les données du token"""
    phone_number: Optional[str] = None 