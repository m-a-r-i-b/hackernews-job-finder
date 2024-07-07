from langchain_core.pydantic_v1 import BaseModel
from pydantic import Extra


class AgentOutput(BaseModel):
    class Config:
        extra = Extra.allow
