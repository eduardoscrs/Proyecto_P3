from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from . import Base
from pydantic import BaseModel

# Esquema Pydantic para la respuesta de una Orden
class OrderResponse(BaseModel):
    id: str
    origen: str
    destino: str
    status: str

    class Config:
        from_attributes = True  

# Modelo SQLAlchemy para el Cliente
class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    total_orders = Column(Integer, default=0)

# Modelo SQLAlchemy para la Orden
class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    origen = Column(String)  # Cambio de "origin" a "origen"
    destino = Column(String)  # Cambio de "destination" a "destino"
    status = Column(String, default="pending")
