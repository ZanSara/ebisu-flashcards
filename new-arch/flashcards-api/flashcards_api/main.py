from fastapi import FastAPI, Depends

app = FastAPI()

from flashcards_api.algorithms.endpoints import router as algorithms_router
from flashcards_api.cards.endpoints import router as cards_router
from flashcards_api.decks.endpoints import router as decks_router
from flashcards_api.facts.endpoints import router as facts_router
from flashcards_api.reviews.endpoints import router as reviews_router
from flashcards_api.tags.endpoints import router as tags_router
from flashcards_api.templates.endpoints import router as templates_router
from flashcards_api.users.endpoints import router as users_router

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
