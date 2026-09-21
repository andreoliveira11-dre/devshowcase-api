from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import repositories, schemas
from app.database import get_db


router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)


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


@router.get(
    "",
    response_model=list[schemas.ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):
    return repositories.get_projects(db)