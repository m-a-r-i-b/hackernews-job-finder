from typing import List
from langchain_core.pydantic_v1 import BaseModel


class KeywordOutput(BaseModel):
    keywords: List[str]


