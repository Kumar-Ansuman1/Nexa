from pydantic import BaseModel


class JoinStep(BaseModel):
    left_dataset: str
    left_column: str
    right_dataset: str
    right_column: str


class JoinPlan(BaseModel):
    joins: list[JoinStep] = []