from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    status: str = "want_to_read"
    rating: Optional[int] = None


class BookUpdate(BaseModel):
    status: Optional[str] = None
    rating: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    status: str
    rating: Optional[int]

    model_config = {"from_attributes": True}