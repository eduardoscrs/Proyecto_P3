from sqlalchemy.orm import Session
from . import models

# =====================
# 📦 CLIENTES
# =====================

def get_all_clients(db: Session):
    return db.query(models.Client).all()

def get_client_by_id(db: Session, client_id: str):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def create_client(db: Session, client: models.Client):
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: str):
    client = get_client_by_id(db, client_id)
    if client:
        db.delete(client)
        db.commit()
    return client

# =====================
# 📦 ÓRDENES
# =====================

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def get_order_by_id(db: Session, order_id: str):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def create_order(db: Session, order: models.Order):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: str):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order
