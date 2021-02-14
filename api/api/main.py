from fastapi import FastAPI, Depends
from api.database import Base, SessionLocal, engine

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

from api.algorithms.endpoints import router as algorithms_router
from api.cards.endpoints import router as cards_router
from api.decks.endpoints import router as decks_router
from api.facts.endpoints import router as facts_router
from api.reviews.endpoints import router as reviews_router
from api.tags.endpoints import router as tags_router
from api.templates.endpoints import router as templates_router
from api.users.endpoints import router as users_router

app.include_router(algorithms_router)
app.include_router(cards_router)
app.include_router(decks_router)
app.include_router(facts_router)
app.include_router(reviews_router)
app.include_router(tags_router)
app.include_router(templates_router)
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}