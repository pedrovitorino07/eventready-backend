from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.favorite import Favorite
from sqlalchemy.exc import IntegrityError


def toggle_favorite(db: Session, user_id: int, event_id: int) -> bool:
    fav = db.query(Favorite).filter(Favorite.user_id == user_id,
                                    Favorite.event_id == event_id).first()

    if fav:
        db.delete(fav)
        db.commit()
        return False
    else:
        new_fav = Favorite(user_id=user_id, event_id=event_id)
        db.add(new_fav)
        try:
            db.commit()
            return True
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Evento ou Usuário não encontrado")


def is_favorited(db: Session, user_id: int, event_id: int) -> bool:
    return db.query(Favorite).filter(Favorite.user_id == user_id, Favorite.event_id == event_id).first() is not None


def get_user_favorites(db: Session, user_id: int):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()
