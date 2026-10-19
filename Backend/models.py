from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Movies(Base):
    __tablename__ = "Movie_Watchlist"

    id : Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    genre: Mapped[str] = mapped_column(String(100))
    rating: Mapped[float]
    views: Mapped[float] 
    release_year: Mapped[int]

# class User(Base):
#     __tablename__ = "Users"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(String(100))
#     email: Mapped[str] = mapped_column(String(100))
#     age: Mapped[int]

