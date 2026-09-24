from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models
from app.database import Base, engine
from app.exceptions import AppException
from app.routes import profiles, projects, technologies


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DevShowcase API",
    description=(
        "API para gerenciamento de perfis, projetos, "
        "tecnologias e feedbacks."
    ),
    version="2.0.0"
)


# ==========================================
# TRATAMENTO DOS ERROS PERSONALIZADOS
# ==========================================

@app.exception_handler(AppException)
async def app_exception_handler(
    request: Request,
    exc: AppException
):
    error_name = (
        "Bad Request"
        if exc.status_code == 400
        else "Not Found"
        if exc.status_code == 404
        else "Error"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": error_name,
            "message": exc.message
        }
    )


# ==========================================
# TRATAMENTO DOS ERROS HTTP
# ==========================================

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    error_name = (
        "Bad Request"
        if exc.status_code == 400
        else "Not Found"
        if exc.status_code == 404
        else "HTTP Error"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "error": error_name,
            "message": str(exc.detail)
        }
    )


# ==========================================
# TRATAMENTO DOS ERROS DE VALIDAÇÃO
# ==========================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    details = []

    for error in exc.errors():
        field = ".".join(
            str(item)
            for item in error["loc"]
        )

        details.append({
            "field": field,
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=400,
        content={
            "status": 400,
            "error": "Bad Request",
            "message": "Dados da requisição inválidos.",
            "details": details
        }
    )


# ==========================================
# ROTAS
# ==========================================

app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


@app.get("/")
def inicio():
    return {
        "mensagem": "DevShowcase API funcionando!"
    }