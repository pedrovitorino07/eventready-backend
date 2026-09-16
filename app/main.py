from fastapi import FastAPI

from app.database import Base, engine
from app.models.evento import Evento
from app.routers import evento

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EventReady API")

app.include_router(evento.router)
