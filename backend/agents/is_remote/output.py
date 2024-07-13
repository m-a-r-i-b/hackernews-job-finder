from langchain_core.pydantic_v1 import BaseModel


class IsRemoteOutput(BaseModel):
    allows_remote_work: bool


