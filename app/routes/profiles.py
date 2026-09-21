from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import repositories, schemas
from app.database import get_db


router = APIRouter(
    prefix="/api/profiles",
    tags=["Profiles"]
)


@router.post(
    "",
    response_model=schemas.ProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    dados: schemas.ProfileCreate,
    db: Session = Depends(get_db)
):
    profile = repositories.create_profile(
        db=db,
        name=dados.name,
        bio=dados.bio,
        github_url=str(dados.github_url)
    )

    return profile


@router.get(
    "/{profile_id}",
    response_model=schemas.ProfileResponse
)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
):
    profile = repositories.get_profile(
        db=db,
        profile_id=profile_id
    )

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil não encontrado."
        )

    return profile