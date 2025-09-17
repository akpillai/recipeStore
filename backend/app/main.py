import os
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Recipe
from .schemas import RecipeCreate, RecipeOut, AIAsk
from .ai_service import AIService

app = FastAPI(title="Recipes API", version="0.1.0")

# CORS
origins = [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables if not exist
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/recipes", response_model=RecipeOut, status_code=201)
def create_recipe(payload: RecipeCreate, db: Session = Depends(get_db)):
    ingredients_text = "\n".join(payload.ingredients) if payload.ingredients else None
    steps_text = "\n".join(payload.steps) if payload.steps else None
    rec = Recipe(
        name=payload.name,
        cuisine=payload.cuisine,
        ingredients=payload.ingredients,
        steps=payload.steps,
        tags=payload.tags,
        source=payload.source,
        image_url=payload.image_url,
        ingredients_text=ingredients_text,
        steps_text=steps_text,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@app.get("/recipes", response_model=List[RecipeOut])
def search_recipes(
    q: Optional[str] = Query(None, description="Search term for name/ingredients"),
    cuisine: Optional[str] = None,
    db: Session = Depends(get_db),
    limit: int = 25,
    offset: int = 0,
):
    stmt = select(Recipe)
    if q:
        like = f"%{q.lower()}%"
        # Simple case-insensitive LIKE on name/ingredients/steps
        stmt = stmt.where(
            (Recipe.name.ilike(like)) |
            (Recipe.ingredients_text.ilike(like)) |
            (Recipe.steps_text.ilike(like))
        )
    if cuisine:
        stmt = stmt.where(Recipe.cuisine.ilike(f"%{cuisine.lower()}%"))
    stmt = stmt.offset(offset).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows

@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    rec = db.get(Recipe, recipe_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return rec

@app.post("/ai/ask")
def ai_ask(payload: AIAsk, db: Session = Depends(get_db)):
    ai = AIService()
    if payload.recipe_name:
        # Try to find the recipe locally first
        stmt = select(Recipe).where(Recipe.name.ilike(f"%{payload.recipe_name}%")).limit(1)
        rec = db.execute(stmt).scalars().first()
        if rec:
            prompt = f"Summarize this recipe and provide tips/substitutions:\nName: {rec.name}\nCuisine: {rec.cuisine}\nIngredients: {rec.ingredients}\nSteps: {rec.steps}"
            answer = ai.summarize_or_answer(prompt)
            return {"source": "database+ai", "answer": answer, "recipe_id": rec.id}
        # Not found, ask AI to propose one
        prompt = f"Provide a clear recipe for '{payload.recipe_name}'. Include ingredients list and numbered steps. Keep it concise."
        answer = ai.summarize_or_answer(prompt)
        return {"source": "ai", "answer": answer}
    elif payload.question:
        answer = ai.summarize_or_answer(payload.question)
        return {"source": "ai", "answer": answer}
    else:
        raise HTTPException(status_code=400, detail="Provide recipe_name or question.")
