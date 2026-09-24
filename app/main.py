from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import event, favorites

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event.router)
app.include_router(favorites.router)


@app.get("/")
def read_root():
    return {"message": "CORS habilitado com sucesso!"}
