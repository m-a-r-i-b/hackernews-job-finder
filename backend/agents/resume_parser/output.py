from langchain_core.pydantic_v1 import BaseModel


class ResumeParserOutput(BaseModel):
    resume_details: str


