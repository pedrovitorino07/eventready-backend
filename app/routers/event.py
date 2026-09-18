import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.event import Evento
from app.schemas.event import (
    EventoCreate,
    EventoResponse,
    EventoUpdate,
    EventoResponseCompleto
)
from app.services.weather import (
    formatar_resposta_clima,
    obter_coordenadas,
    obter_previsao_clima,
)
from app.services.climate_analysis_service import analisar_clima
from app.services.event_score_service import calcular_event_score
from app.services.favorite_service import is_favorited

router = APIRouter(prefix="/eventos", tags=["Eventos"])


class MockUser(BaseModel):
    id: int


def get_current_user():
    return MockUser(id=1)


def converter_clima_para_numerico(clima_dict: dict) -> dict:
    """Converte os valores de clima com strings/unidades para tipos numéricos puros."""
    def parse_float(val):
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", val.replace(',', '.'))
            return float(nums[0]) if nums else 0.0
        return 0.0

    def parse_int(val):
        if isinstance(val, (int, float)):
            return int(val)
        if isinstance(val, str):
            nums = re.findall(r"\d+", val)
            return int(nums[0]) if nums else 0
        return 0

    return {
        "condicao": clima_dict.get("condicao", "Desconhecida"),
        "temperatura_max": parse_float(clima_dict.get("temperatura_max", 0)),
        "sensacao_max": parse_float(clima_dict.get("sensacao_max", 0)),
        "chance_chuva": parse_int(clima_dict.get("chance_chuva", 0)),
        "vento_max": parse_float(clima_dict.get("vento_max", 0)),
        "indice_uv_max": parse_float(clima_dict.get("indice_uv_max", 0)),
        "sol": clima_dict.get("sol", {"nascer": "00:00", "por": "00:00"})
    }


@router.post(
    "/", response_model=EventoResponse, status_code=status.HTTP_201_CREATED
)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    dados_evento = evento.model_dump()

    if not dados_evento.get("latitude") or not dados_evento.get("longitude"):
        lat, lon = obter_coordenadas(dados_evento["local"])
        if lat and lon:
            dados_evento["latitude"] = lat
            dados_evento["longitude"] = lon

    db_evento = Evento(**dados_evento)
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento


@router.get("/", response_model=List[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).all()


@router.get("/{evento_id}/clima", response_model=EventoResponseCompleto)
def buscar_evento_por_id(
    evento_id: int,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(get_current_user)
):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    if not evento.latitude or not evento.longitude:
        raise HTTPException(
            status_code=400,
            detail="Evento não possui coordenadas geográficas registradas.",
        )

    data_str = evento.data.strftime("%Y-%m-%d")
    clima_raw, erro = obter_previsao_clima(
        float(evento.latitude), float(evento.longitude), data_str
    )

    if erro:
        raise HTTPException(
            status_code=400,
            detail=f"Não foi possível obter dados do clima: {erro}",
        )

    clima_data = formatar_resposta_clima(evento.nome, clima_raw)
    if isinstance(clima_data, dict) and "recomendacao" in clima_data:
        clima_data.pop("recomendacao")

    analise_climatica = analisar_clima(clima_data)

    horario_formatado = evento.horario.strftime("%H:%M") if hasattr(
        evento.horario, 'strftime') else str(evento.horario)[:5]

    event_score_data = calcular_event_score(clima_data, horario_formatado)

    favoritado = is_favorited(db, current_user.id, evento_id)

    return {
        "evento": {
            "id": evento.id,
            "nome": evento.nome,
            "data": evento.data,
            "horario": horario_formatado,
            "local": evento.local,
            "latitude": evento.latitude,
            "longitude": evento.longitude
        },
        "clima": clima_data,
        "analise_climatica": analise_climatica,
        "event_score": event_score_data,
        "favoritado": favoritado
    }


@router.delete("/{evento_id}", status_code=status.HTTP_200_OK)
def deletar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado.",
        )

    db.delete(evento)
    db.commit()

    return {"message": "Evento deletado com sucesso."}


@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(
    evento_id: int,
    evento_in: EventoUpdate,
    db: Session = Depends(get_db),
):
    db_evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado.",
        )

    dados_atualizacao = evento_in.model_dump(exclude_unset=True)

    if "local" in dados_atualizacao and (
        "latitude" not in dados_atualizacao or "longitude" not in dados_atualizacao
    ):
        lat, lon = obter_coordenadas(dados_atualizacao["local"])
        if lat and lon:
            dados_atualizacao["latitude"] = lat
            dados_atualizacao["longitude"] = lon

    for campo, valor in dados_atualizacao.items():
        setattr(db_evento, campo, valor)

    db.commit()
    db.refresh(db_evento)

    return db_evento
