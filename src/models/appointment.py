from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel

class AppointmentStatus(enum.Enum):
    """Statuts possibles d'un rendez-vous"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class Appointment(BaseModel):
    """Modèle pour les rendez-vous médicaux"""
    __tablename__ = "appointments"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    
    appointment_date = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)
    symptoms = Column(Text)
    notes = Column(Text)
    priority = Column(String(20))  # normal, urgent, emergency
    
    # Informations de suivi
    reminder_sent = Column(Boolean, default=False)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    
    # Relations
    user = relationship("User", back_populates="appointments")
    hospital = relationship("Hospital", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments") 