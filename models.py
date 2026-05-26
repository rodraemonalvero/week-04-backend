from database import Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)