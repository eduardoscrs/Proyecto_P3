from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from pydantic import BaseModel

class OrderResponse(BaseModel):
    id: str
    origen: str
    destino: str
    status: str

    class Config:
        orm_mode = True  # Permite que SQLAlchemy y Pydantic trabajen juntos

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    total_orders = Column(Integer, default=0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    origen = Column(String)
    destino = Column(String)
    status = Column(String, default="pending")