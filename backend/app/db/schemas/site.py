from pydantic import BaseModel, HttpUrl


class SiteCreate(BaseModel):
    url: HttpUrl
    label: str | None = None


class SiteOut(BaseModel):
    id: int
    url: str
    label: str | None

    class Config:
        from_attributes = True



