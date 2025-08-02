from enum import Enum
from typing import List
from pydantic import BaseModel, Field, validator


class HeatingMode(str, Enum):
    """Les différents modes de chauffage possibles"""
    ECO = "ECO"
    CONFORT = "CONFORT"
    OFF = "OFF"

    @classmethod
    def _missing_(cls, value: str):
        """Permet de gérer les variations de casse"""
        value = value.upper()
        for member in cls:
            if member.value == value:
                return member
        return None  # Valeur invalide


class WeekSchedule(BaseModel):
    """Le planning de la semaine"""
    monday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    tuesday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    wednesday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    thursday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    friday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    saturday: List[HeatingMode] = Field(..., min_items=96, max_items=96)
    sunday: List[HeatingMode] = Field(..., min_items=96, max_items=96)

    @validator('*', pre=True)
    def convert_case(cls, v):
        """Convertit les modes en majuscules pour la validation"""
        if isinstance(v, list):
            return [x.upper() if isinstance(x, str) else x for x in v]
        return v

    @classmethod
    def get_default_schedule(cls) -> 'WeekSchedule':
        """Crée un planning par défaut avec tous les créneaux en ECO"""
        return cls(
            monday=[HeatingMode.ECO] * 96,
            tuesday=[HeatingMode.ECO] * 96,
            wednesday=[HeatingMode.ECO] * 96,
            thursday=[HeatingMode.ECO] * 96,
            friday=[HeatingMode.ECO] * 96,
            saturday=[HeatingMode.ECO] * 96,
            sunday=[HeatingMode.ECO] * 96,
        )


class ScheduleUpdate(BaseModel):
    """Le modèle pour la mise à jour du planning"""
    schedule: WeekSchedule
