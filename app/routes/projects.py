from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import repositories, schemas, services
from app.database import get_db


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


# =========================
# CRIAR PROJETO
# =========================

@router.post(
    "",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    dados: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    project = repositories.create_project(
        db=db,
        title=dados.title,
        description=dados.description,
        repository_url=str(dados.repository_url),
        profile_id=dados.profile_id,
        technology_ids=dados.technology_ids
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil não encontrado."
        )

    return project


# =========================
# LISTAR PROJETOS
# FILTRO + PAGINAÇÃO
# =========================

@router.get(
    "",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    technology: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return repositories.get_projects(
        db=db,
        technology=technology,
        page=page,
        size=size
    )


# =========================
# CADASTRAR FEEDBACK
# =========================

@router.post(
    "/{project_id}/feedbacks",
    response_model=schemas.FeedbackResponse,
    status_code=status.HTTP_201_CREATED
)
def create_feedback(
    project_id: int,
    dados: schemas.FeedbackCreate,
    db: Session = Depends(get_db)
):
    project = repositories.get_project(
        db=db,
        project_id=project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado."
        )

    feedback = repositories.create_feedback(
        db=db,
        project_id=project_id,
        author=dados.author,
        comment=dados.comment,
        rating=dados.rating
    )

    services.calculate_average_rating(
        db=db,
        project=project
    )

    return feedback


# =========================
# UPVOTE
# =========================

@router.put(
    "/{project_id}/upvote",
    response_model=schemas.ProjectResponse
)
def upvote_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = repositories.get_project(
        db=db,
        project_id=project_id
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Projeto não encontrado."
        )

    project = services.increment_upvote(
        db=db,
        project=project
    )

    return project