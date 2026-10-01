from pydantic import BaseModel


class JevSelection(BaseModel):
    metric: str | None = None
    dimensions: list[str] = []