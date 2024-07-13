from langchain_core.pydantic_v1 import BaseModel


class TestOutput(BaseModel):
    allows_remote_work: bool


