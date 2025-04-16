from sqlalchemy import Column, String, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    """Modèle pour les utilisateurs de l'application"""
    __tablename__ = "users"

    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    language_preference = Column(String(10), default="fr")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    preferences = Column(JSON, default=dict)
    
    # Relations
    appointments = relationship("Appointment", back_populates="user")
    emergency_contacts = relationship("EmergencyContact", back_populates="user") 