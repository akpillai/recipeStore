from typing import List, Optional
from pydantic import BaseModel, Field

class RecipeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    cuisine: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    image_url: Optional[str] = None

class RecipeOut(BaseModel):
    id: int
    name: str
    cuisine: Optional[str] = None
    ingredients: Optional[List[str]] = None
    steps: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class AIAsk(BaseModel):
    recipe_name: str | None = None
    question: str | None = None
