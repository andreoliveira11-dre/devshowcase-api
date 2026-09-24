from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


# =========================
# PROFILE
# =========================

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    bio: str | None = None
    github_url: HttpUrl

    @field_validator("name")
    @classmethod
    def validar_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("O nome não pode estar vazio.")

        return value


class ProfileResponse(BaseModel):
    id: int
    name: str
    bio: str | None
    github_url: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# TECHNOLOGY
# =========================

class TechnologyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def validar_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "O nome da tecnologia não pode estar vazio."
            )

        return value


class TechnologyResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# FEEDBACK
# =========================

class FeedbackCreate(BaseModel):
    author: str = Field(min_length=1, max_length=100)
    comment: str = Field(min_length=1)
    rating: int = Field(ge=1, le=5)

    @field_validator("author", "comment")
    @classmethod
    def validar_texto(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "O campo não pode estar vazio."
            )

        return value


class FeedbackResponse(BaseModel):
    id: int
    author: str
    comment: str
    rating: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# PROJECT
# =========================

class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    repository_url: HttpUrl
    profile_id: int = Field(gt=0)
    technology_ids: list[int] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validar_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "O título não pode estar vazio."
            )

        return value


class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    repository_url: str
    profile_id: int

    technologies: list[TechnologyResponse]

    average_rating: float
    upvotes: int

    model_config = ConfigDict(from_attributes=True)