from typing import Dict, Union
from pydantic import BaseModel
from const import Step

class ThreadDetails(BaseModel):
    title: str
    url: str

class Experience(BaseModel):
    experience: str

class Criteria(BaseModel):
    mandatory: str
    optional: str



class SocketMessage(BaseModel):
    thread_url: str
    comment_id: str
    payload: Dict[Step, str]