from enum import Enum
from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import Extra


class AgentObservation(str, Enum):
    STEP_COMPLETED = "STEP_COMPLETED"
    TAKE_USER_INPUT = "TAKE_USER_INPUT"

    def __str__(self) -> str:
        return str.__str__(self)


class AgentOutputData(BaseModel):
    message: str = Field(description="agent's output message")

    class Config:
        extra = Extra.allow


class AgentOutput(BaseModel):
    observation: AgentObservation = Field(
        description="agent's observation about current step, whether its completed or requires additional input from user to complete it"
    )
    data: AgentOutputData
