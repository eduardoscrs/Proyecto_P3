from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    total_orders = Column(Integer, default=0)

    orders = relationship("Order", back_populates="client")

class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True, index=True)
    origin = Column(String)
    destination = Column(String)
    priority = Column(Integer)

    client_id = Column(String, ForeignKey("clients.id"))
    client = relationship("Client", back_populates="orders")
