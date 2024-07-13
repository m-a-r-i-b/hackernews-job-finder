from typing import List
from langchain_core.pydantic_v1 import BaseModel


class RoleOutput(BaseModel):
    roles: List[str]


