from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, time


class SolSchema(BaseModel):
    nascer: str
    por: str


class ClimaSchema(BaseModel):
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


class EventScoreFatoresSchema(BaseModel):
    clima: int
    chuva: int
    temperatura: int
    horario: int
    uv: int


class EventScoreSchema(BaseModel):
    score: int
    nivel: str
    fatores: EventScoreFatoresSchema


class EventoDetalheSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    data: date
    horario: time
    local: str


class EventoResponseCompleto(BaseModel):
    evento: EventoDetalheSchema
    clima: Optional[ClimaSchema] = None
    analise_climatica: Optional[AnaliseClimaticaSchema] = None
    event_score: Optional[EventScoreSchema] = None
    favoritado: bool = False


class FavoriteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    event_id: int


class EventoBase(BaseModel):
    nome: str
    data: date
    horario: time
    local: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    descricao: Optional[str] = None


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    nome: Optional[str] = None
    data: Optional[date] = None
    horario: Optional[time] = None
    local: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    descricao: Optional[str] = None


class EventoResponse(EventoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
