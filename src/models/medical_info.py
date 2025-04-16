from sqlalchemy import Column, String, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class MedicalInfo(BaseModel):
    """Modèle pour les informations médicales"""
    __tablename__ = "medical_info"

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    category = Column(String(50), nullable=False)
    
    # Métadonnées
    tags = Column(JSON, default=list)
    source = Column(String(255))
    author = Column(String(255))
    last_reviewed = Column(String(255))
    
    # Relations
    related_diseases = Column(JSON, default=list)  # Maladies associées
    symptoms = Column(JSON, default=list)  # Symptômes associés
    treatments = Column(JSON, default=list)  # Traitements recommandés
    
    # Accessibilité
    audio_content = Column(String(255))  # URL vers la version audio
    video_content = Column(String(255))  # URL vers la version vidéo
    image_content = Column(JSON, default=list)  # URLs vers les images 