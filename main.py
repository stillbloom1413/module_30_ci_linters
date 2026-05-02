from contextlib import asynccontextmanager
from typing import List, Sequence

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import Base, async_session, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


async def get_db():
    async with async_session() as session:
        yield session


@app.get("/recipes", response_model=List[schemas.RecipeList])
async def get_recipes_list(
    db: AsyncSession = Depends(get_db),
) -> Sequence[models.Recipe]:
    recipes = await db.execute(
        select(models.Recipe).order_by(
            models.Recipe.views_count.desc(), models.Recipe.cooking_time
        )
    )
    return recipes.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
async def get_recipe(
    recipe_id: int, db: AsyncSession = Depends(get_db)
) -> schemas.Recipe:
    query = await db.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
    result = query.scalars().one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    result.views_count += 1
    await db.commit()
    await db.refresh(result)
    return result


@app.post("/recipes", response_model=schemas.Recipe)
async def create_recipe(
    recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)
) -> schemas.Recipe:
    new_recipe = models.Recipe(**recipe.model_dump())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe
