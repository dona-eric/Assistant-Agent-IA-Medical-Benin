from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .base import IDSchema, TimestampSchema
from ..models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    """Schéma de base pour les rendez-vous"""
    appointment_date: datetime
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    priority: str = "normal"  # normal, urgent, emergency

class AppointmentCreate(AppointmentBase):
    """Schéma pour la création de rendez-vous"""
    user_id: int
    hospital_id: int
    doctor_id: Optional[int] = None

class AppointmentUpdate(BaseModel):
    """Schéma pour la mise à jour de rendez-vous"""
    appointment_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    symptoms: Optional[str] = None
    notes: Optional[str] = None
    priority: Optional[str] = None
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[datetime] = None

class AppointmentInDB(IDSchema, TimestampSchema, AppointmentBase):
    """Schéma pour les données de rendez-vous en base"""
    user_id: int
    hospital_id: int
    doctor_id: Optional[int]
    status: AppointmentStatus
    reminder_sent: bool
    follow_up_required: bool
    follow_up_date: Optional[datetime]

class AppointmentResponse(AppointmentInDB):
    """Schéma pour la réponse API"""
    pass

class AppointmentFilter(BaseModel):
    """Schéma pour le filtrage des rendez-vous"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    priority: Optional[str] = None
    hospital_id: Optional[int] = None
    user_id: Optional[int] = None 