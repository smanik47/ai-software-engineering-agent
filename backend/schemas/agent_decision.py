
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AgentArguments(BaseModel):

    model_config = ConfigDict(extra="forbid")

    path: str | None = None


class AgentDecision(BaseModel):

    model_config = ConfigDict(extra="forbid")

    action: Literal[
        "inspect_repository",
        "read_file",
        "finish"
    ]

    arguments: AgentArguments = Field(
        default_factory=AgentArguments
    )

    reason: str

    status: Literal[
        "continue",
        "completed"
    ]
