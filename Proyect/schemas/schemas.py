from pydantic import BaseModel
from typing import Optional

# Esquema para Cliente (Client)
class ClientBase(BaseModel):
    name: str
    total_orders: int

    class Config:
        orm_mode = True  # Permite que Pydantic use el modelo de SQLAlchemy directamente

class ClientResponse(ClientBase):
    id: str  # Campo solo para la respuesta, no en la creación

# Esquema para Orden (Order)
class OrderBase(BaseModel):
    origen: str
    destino: str
    status: str

    class Config:
        orm_mode = True  # Permite que Pydantic use el modelo de SQLAlchemy directamente

class OrderResponse(OrderBase):
    id: str  # Campo solo para la respuesta, no en la creación
