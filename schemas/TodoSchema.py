from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class TodoCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(min_length=3, max_length=100, default=None)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: int
    complete: bool

    model_config = ConfigDict(from_attributes=True)