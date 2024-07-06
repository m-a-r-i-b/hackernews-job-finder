from pydantic import BaseModel

class ThreadDetails(BaseModel):
    title: str
    url: str

class Experience(BaseModel):
    experience: str

class Criteria(BaseModel):
    mandatory: str
    optional: str