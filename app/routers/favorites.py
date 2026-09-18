from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.services import favorite_service
from app.models.favorite import Favorite

router = APIRouter(prefix="/eventos", tags=["Favoritos"])


class MockUser(BaseModel):
    id: int


def get_current_user():
    return MockUser(id=1)


@router.post("/{event_id}/favoritar")
def favoritar_evento(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(get_current_user)
):
    try:
        favorito_existente = db.query(Favorite).filter(
            Favorite.user_id == current_user.id,
            Favorite.event_id == event_id
        ).first()

        if favorito_existente:
            return {"mensagem": "O evento já está nos favoritos", "favoritado": True}

        novo_fav = Favorite(user_id=current_user.id, event_id=event_id)
        db.add(novo_fav)
        db.commit()
        return {"mensagem": "Evento favoritado com sucesso", "favoritado": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao favoritar evento")


@router.delete("/{event_id}/favoritar", status_code=status.HTTP_200_OK)
def desfavoritar_evento(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(get_current_user)
):
    fav = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.event_id == event_id
    ).first()

    if not fav:
        raise HTTPException(
            status_code=404, detail="Este evento não está nos seus favoritos")

    db.delete(fav)
    db.commit()

    return {"message": "Evento removido dos favoritos com sucesso."}


@router.get("/favoritos")
def listar_favoritos(
    db: Session = Depends(get_db),
    current_user: MockUser = Depends(get_current_user)
):
    return favorite_service.get_user_favorites(db, current_user.id)
