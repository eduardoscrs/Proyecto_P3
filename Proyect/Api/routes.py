from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Proyect.data.models import Order  # Tu modelo de SQLAlchemy
from Proyect.data.dependencies import get_db
from schemas import OrderResponse  # Asegúrate de importar el modelo Pydantic

app = FastAPI()

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order  # FastAPI convierte automáticamente 'order' al modelo Pydantic OrderResponse
