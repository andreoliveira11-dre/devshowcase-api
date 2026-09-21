from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import repositories, schemas
from app.database import get_db


router = APIRouter(
    prefix="/api/technologies",
    tags=["Technologies"]
)


@router.post(
    "",
    response_model=schemas.TechnologyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_technology(
    dados: schemas.TechnologyCreate,
    db: Session = Depends(get_db)
):
    try:
        technology = repositories.create_technology(
            db=db,
            name=dados.name
        )

        return technology

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Essa tecnologia já está cadastrada."
        )


@router.get(
    "",
    response_model=list[schemas.TechnologyResponse]
)
def get_technologies(
    db: Session = Depends(get_db)
):
    return repositories.get_technologies(db)