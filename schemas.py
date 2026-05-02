from pydantic import BaseModel


class RecipeBase(BaseModel):
    name: str
    cooking_time: int


class RecipeList(RecipeBase):
    id: int
    views_count: int

    class Config:
        from_attributes = True


class Recipe(RecipeBase):
    id: int
    ingredients: str
    description: str

    class Config:
        from_attributes = True


class RecipeCreate(RecipeBase):
    ingredients: str
    description: str
