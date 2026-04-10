from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Joke(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    author = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
