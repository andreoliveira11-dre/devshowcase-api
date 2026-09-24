from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.database import Base


project_technology = Table(
    "project_technology",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("projects.id"),
        primary_key=True
    ),
    Column(
        "technology_id",
        Integer,
        ForeignKey("technologies.id"),
        primary_key=True
    )
)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    github_url = Column(String(255), nullable=False)

    projects = relationship(
        "Project",
        back_populates="profile"
    )


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    repository_url = Column(String(255), nullable=False)

    profile_id = Column(
        Integer,
        ForeignKey("profiles.id"),
        nullable=False
    )

    # NOVO NA ATIVIDADE 2
    average_rating = Column(
        Float,
        nullable=False,
        default=0.0
    )

    # NOVO NA ATIVIDADE 2
    upvotes = Column(
        Integer,
        nullable=False,
        default=0
    )

    profile = relationship(
        "Profile",
        back_populates="projects"
    )

    technologies = relationship(
        "Technology",
        secondary=project_technology,
        back_populates="projects"
    )

    feedbacks = relationship(
        "Feedback",
        back_populates="project"
    )


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)

    projects = relationship(
        "Project",
        secondary=project_technology,
        back_populates="technologies"
    )


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(100), nullable=False)
    comment = Column(Text, nullable=False)

    # NOVO NA ATIVIDADE 2
    rating = Column(
        Integer,
        nullable=False
    )

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="feedbacks"
    )