from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """Schéma de base avec configuration commune"""
    model_config = ConfigDict(from_attributes=True)

class TimestampSchema(BaseSchema):
    """Schéma avec horodatage"""
    created_at: datetime
    updated_at: datetime

class IDSchema(BaseSchema):
    """Schéma avec ID"""
    id: int 