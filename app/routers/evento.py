from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoResponse
from app.services.weather import (
    formatar_resposta_clima,
    obter_coordenadas,
    obter_previsao_clima,
)

router = APIRouter(prefix="/eventos", tags=["Eventos"])


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


@router.get("/{evento_id}/clima")
def ver_clima_do_evento(evento_id: int, db: Session = Depends(get_db)):
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

    return formatar_resposta_clima(evento.nome, clima_raw)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()

    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado.",
        )

    db.delete(evento)
    db.commit()

    return None


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
