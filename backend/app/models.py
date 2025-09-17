from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.types import JSON
from .database import Base, DATABASE_URL

# Choose JSON type based on DB dialect
if DATABASE_URL.startswith("postgresql"):
    from sqlalchemy.dialects.postgresql import JSONB
    RecipeJSON = JSONB
else:
    RecipeJSON = JSON  # SQLite or other DBs
    
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    cuisine = Column(String(100), nullable=True, index=True)
    ingredients = Column(RecipeJSON, nullable=True)  # list of strings
    steps = Column(RecipeJSON, nullable=True)        # list of strings
    tags = Column(RecipeJSON, nullable=True)         # list of strings
    source = Column(String(255), nullable=True)
    image_url = Column(String(512), nullable=True)
    ingredients_text = Column(Text, nullable=True)   # for simple LIKE search
    steps_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
