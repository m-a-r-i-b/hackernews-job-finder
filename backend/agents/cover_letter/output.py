from langchain_core.pydantic_v1 import BaseModel


class CoverLetterOutput(BaseModel):
    cover_letter: str


