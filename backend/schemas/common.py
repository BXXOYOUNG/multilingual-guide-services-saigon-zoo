from pydantic import BaseModel, Field


class APIErrorDetail(BaseModel):
    location: list[str | int] | None = None
    message: str
    type: str | None = None


class APIErrorBody(BaseModel):
    code: str
    message: str
    details: list[APIErrorDetail] = Field(default_factory=list)


class APIErrorResponse(BaseModel):
    error: APIErrorBody