from datetime import date, time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class EventoBase(BaseModel):
    nome: str
    data: date
    horario: time
    local: str
    descricao: Optional[str] = None


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    data: Optional[date] = None
    horario: Optional[time] = None
    local: Optional[str] = None
    descricao: Optional[str] = None


class EventoResponse(EventoBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class EventoResponseDetalhado(BaseModel):
    id: int
    nome: str
    data: date
    horario: str
    local: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class SolSchema(BaseModel):
    nascer: str
    por: str


class ClimaNumericoSchema(BaseModel):
    condicao: str
    temperatura_max: float
    sensacao_max: float
    chance_chuva: int
    vento_max: float
    indice_uv_max: float
    sol: SolSchema


class AnaliseClimaticaSchema(BaseModel):
    nivel: str
    motivos: List[str]
    recomendacoes: List[str]


class EventScoreSchema(BaseModel):
    score: int
    nivel: str
    fatores: Dict[str, Any]


class EventoResponseCompleto(BaseModel):
    evento: EventoResponseDetalhado
    clima: ClimaNumericoSchema
    analise_climatica: AnaliseClimaticaSchema
    event_score: EventScoreSchema
    favoritado: bool
