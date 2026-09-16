from datetime import date, time
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, field_serializer


class EventoBase(BaseModel):
    nome: str
    data: date
    horario: time
    local: str
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    descricao: Optional[str] = None

    @field_serializer("horario")
    def serialize_horario(self, horario: Optional[time], _info) -> Optional[str]:
        if horario is not None:
            return horario.strftime("%H:%M")
        return None


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    data: Optional[date] = None
    horario: Optional[time] = None
    local: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    descricao: Optional[str] = None

    @field_serializer("horario")
    def serialize_horario(self, horario: Optional[time], _info) -> Optional[str]:
        if horario is not None:
            return horario.strftime("%H:%M")
        return None


class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True
