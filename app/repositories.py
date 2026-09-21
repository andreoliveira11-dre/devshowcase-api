from sqlalchemy.orm import Session

from app import models


# =========================
# PROFILE
# =========================

def create_profile(
    db: Session,
    name: str,
    bio: str | None,
    github_url: str
):
    profile = models.Profile(
        name=name,
        bio=bio,
        github_url=github_url
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def get_profile(db: Session, profile_id: int):
    return (
        db.query(models.Profile)
        .filter(models.Profile.id == profile_id)
        .first()
    )


# =========================
# TECHNOLOGY
# =========================

def create_technology(db: Session, name: str):
    technology = models.Technology(
        name=name
    )

    db.add(technology)
    db.commit()
    db.refresh(technology)

    return technology


def get_technologies(db: Session):
    return db.query(models.Technology).all()


# =========================
# PROJECT
# =========================

def create_project(
    db: Session,
    title: str,
    description: str | None,
    repository_url: str,
    profile_id: int,
    technology_ids: list[int]
):
    profile = (
        db.query(models.Profile)
        .filter(models.Profile.id == profile_id)
        .first()
    )

    if profile is None:
        return None

    technologies = (
        db.query(models.Technology)
        .filter(models.Technology.id.in_(technology_ids))
        .all()
    )

    project = models.Project(
        title=title,
        description=description,
        repository_url=repository_url,
        profile_id=profile_id,
        technologies=technologies
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def get_projects(db: Session):
    return db.query(models.Project).all()