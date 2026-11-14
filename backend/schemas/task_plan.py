
from pydantic import BaseModel, Field


class TaskStep(BaseModel):

    step_number: int

    description: str

    expected_outcome: str


class TaskPlan(BaseModel):

    task: str

    steps: list[TaskStep] = Field(
        min_length=1
    )

    status: str
