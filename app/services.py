from sqlalchemy.orm import Session

from app import models


def calculate_average_rating(
    db: Session,
    project: models.Project
):
    feedbacks = (
        db.query(models.Feedback)
        .filter(models.Feedback.project_id == project.id)
        .all()
    )

    if not feedbacks:
        project.average_rating = 0.0
    else:
        total_rating = sum(
            feedback.rating
            for feedback in feedbacks
        )

        project.average_rating = (
            total_rating / len(feedbacks)
        )

    db.commit()
    db.refresh(project)

    return project.average_rating


def increment_upvote(
    db: Session,
    project: models.Project
):
    project.upvotes += 1

    db.commit()
    db.refresh(project)

    return project