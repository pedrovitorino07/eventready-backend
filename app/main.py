from fastapi import FastAPI

from app.database import Base, engine
from app.models.event import Evento
from app.models.favorite import Favorite
from app.routers import event, favorites

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventReady API")

app.include_router(event.router)
app.include_router(favorites.router)
