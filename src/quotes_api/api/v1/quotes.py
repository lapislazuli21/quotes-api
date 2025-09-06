from typing import List

import redis.asyncio as redis
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...core.auth import get_api_key
from ...core.cache import get_cache
from ...db import models as db_models
from ...db.session import get_db
from ...models.quote_model import Quote, QuoteCreate

router = APIRouter()

# --- API Endpoints ---

@router.post("/quotes", response_model=Quote, status_code=status.HTTP_201_CREATED)
async def add_quote(quote_data: QuoteCreate, db: Session = Depends(get_db),  api_key: str = Depends(get_api_key)):
    """Adds a new quote to the database."""
    new_quote = db_models.Quote(content=quote_data.content, author=quote_data.author)
    db.add(new_quote)
    await db.commit()
    await db.refresh(new_quote)
    return new_quote


@router.get("/quotes", response_model=List[Quote])
async def list_quotes(db: Session = Depends(get_db)):
    """Lists all quotes from the database."""
    result = await db.execute(select(db_models.Quote))
    return result.scalars().all()


@router.get("/quotes/{quote_id}", response_model=Quote)
async def get_quote(quote_id: int, db: Session = Depends(get_db), cache: redis.Redis = Depends(get_cache)):
    """Gets a single quote by its ID from the database."""
    if cache:
        cache_key = f"quote:{quote_id}"
        cached_quote = await cache.get(cache_key)
        if cached_quote:
            return Quote.model_validate_json(cached_quote)

    result = await db.execute(select(db_models.Quote).filter(db_models.Quote.id == quote_id))
    quote = result.scalars().first()
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    if cache:
        await cache.set(f"quote:{quote_id}", Quote.model_validate(quote).model_dump_json(), ex=3600)

    return quote


@router.delete("/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(quote_id: int, db: Session = Depends(get_db), cache: redis.Redis = Depends(get_cache),  api_key: str = Depends(get_api_key)):
    """Deletes a quote by its ID from the database."""
    result = await db.execute(select(db_models.Quote).filter(db_models.Quote.id == quote_id))
    quote = result.scalars().first()
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")

    await db.delete(quote)
    await db.commit()

    if cache:
        await cache.delete(f"quote:{quote_id}")

    return