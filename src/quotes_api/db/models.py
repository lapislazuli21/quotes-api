from sqlalchemy import Column, Integer, String

from .session import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    author = Column(Integer, index=True)