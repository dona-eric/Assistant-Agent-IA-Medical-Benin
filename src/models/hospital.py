from sqlalchemy import Column, String, Float, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Hospital(BaseModel):
    """Modèle pour les établissements de santé"""
    __tablename__ = "hospitals"

    name = Column(String(255), nullable=False, index=True)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    phone_number = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    
    # Informations sur les services
    type = Column(String(50), nullable=False)  # public, private, community
    level = Column(String(50))  # primary, secondary, tertiary
    specialties = Column(JSON, default=list)  # Liste des spécialités
    services = Column(JSON, default=list)  # Liste des services offerts
    working_hours = Column(JSON, default=dict)  # Horaires d'ouverture
    emergency_services = Column(Boolean, default=False)
    
    # Informations supplémentaires
    description = Column(Text)
    facilities = Column(JSON, default=list)  # Équipements disponibles
    insurance_accepted = Column(JSON, default=list)  # Types d'assurance acceptés
    languages_spoken = Column(JSON, default=list)  # Langues parlées par le personnel
    
    # Relations
    appointments = relationship("Appointment", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital") 