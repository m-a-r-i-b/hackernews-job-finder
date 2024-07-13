from typing import List
from langchain_core.pydantic_v1 import BaseModel


class ContactInfoOutput(BaseModel):
    contact_info: List[str]


