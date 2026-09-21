from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routes import profiles, projects, technologies


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DevShowcase API",
    description="API para gerenciamento de perfis, projetos, tecnologias e feedbacks.",
    version="1.0.0"
)


app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


@app.get("/")
def inicio():
    return {
        "mensagem": "DevShowcase API funcionando!"
    }