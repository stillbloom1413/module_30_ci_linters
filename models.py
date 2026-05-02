from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    cooking_time: Mapped[int] = mapped_column(index=True)
    ingredients: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    views_count: Mapped[int] = mapped_column(index=True, default=0)
