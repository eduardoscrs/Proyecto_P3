from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import networkx as nx
from pydantic import BaseModel

# Simulación
from Proyect.sim.simulation import run_simulation_dynamic, dijkstra_shortest_path
from Proyect.sim.serialize_utils import serialize_simulation_result

# Base de datos
from Proyect.data.dependencies import get_db
from Proyect.data.models import Client, Order

# Importar los esquemas Pydantic para las respuestas
from Proyect.schemas.schemas import ClientResponse, OrderResponse, ClientBase, OrderBase

# Router adicional
from Proyect.Api.controllers import router as api_router

app = FastAPI()
app.include_router(api_router)

# ========== Modelos de entrada ==========

class SimulationParams(BaseModel):
    num_nodes: int
    num_edges: int
    num_orders: int

class RouteRequest(BaseModel):
    origen: str
    destino: str

# ========== Endpoints ==========

@app.post("/run_simulation/")
async def run_simulation(params: SimulationParams, db: Session = Depends(get_db)):
    # Llamada al método para generar la simulación con los parámetros proporcionados
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)

    # Guardar CLIENTES
    for client_id, client_obj in result["clientes"].items():
        # Usar 'name' en lugar de 'nombre' para acceder a los atributos correctos
        db_client = Client(id=client_id, name=client_obj.name, total_orders=client_obj.total_orders)
        db.merge(db_client)

    # Guardar ÓRDENES con estado

# Cambio en api.py
    for order in result["orders"]:
        status = "delivered" if getattr(order, "estado", "").lower() == "entregada" else "pending"
        # Cambiar `order.order_id` a `order.id` para que coincida con el modelo de la base de datos
        db_order = Order(id=order.order_id, origen=order.origin, destino=order.destination, status=status)

        db.merge(db_order)



    db.commit()
    return serialize_simulation_result(result)


@app.post("/get_route/")  # Endpoint para obtener una ruta
async def get_route(request: RouteRequest, num_nodes: int = 15, num_edges: int = 20, num_orders: int = 10):
    sim = run_simulation_dynamic(num_nodes, num_edges, num_orders)  # Usar parámetros dinámicos
    nx_graph = sim["nx_graph"]
    if request.origen not in nx_graph or request.destino not in nx_graph:
        raise HTTPException(status_code=400, detail="Origin or destination node not found.")
    
    path = dijkstra_shortest_path(nx_graph, request.origen, request.destino)
    if not path:
        raise HTTPException(status_code=404, detail="No path found between the nodes.")
    return {"path": path}


@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}

# Endpoints de clientes

@app.get("/clients/", response_model=list[ClientResponse])
async def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients  # FastAPI convertirá estos objetos a ClientResponse automáticamente

@app.get("/clients/{client_id}", response_model=ClientResponse)
async def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client  # FastAPI convertirá estos objetos a ClientResponse automáticamente

class UpdateClient(BaseModel):
    name: str
    total_orders: int

@app.put("/clients/{client_id}")
async def update_client(client_id: str, update_data: UpdateClient, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.name = update_data.name
    client.total_orders = update_data.total_orders
    db.commit()
    return {"message": f"Client {client_id} updated successfully"}

@app.delete("/clients/{client_id}")
async def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    db.delete(client)
    db.commit()
    return {"message": f"Client {client_id} deleted successfully"}

# Endpoints de órdenes

@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order  # FastAPI convertirá estos objetos a OrderResponse automáticamente

@app.post("/orders/{order_id}/cancel")
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "cancelled"
    db.commit()
    return {"message": f"Order {order_id} has been cancelled"}

@app.post("/orders/{order_id}/complete")
async def complete_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = "delivered"
    db.commit()
    return {"message": f"Order {order_id} has been completed"}

# Nuevos endpoints añadidos para obtener, cancelar y completar órdenes

@app.get("/orders/", response_model=list[OrderResponse])
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders  # FastAPI convertirá estos objetos a OrderResponse automáticamente

@app.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderBase, db: Session = Depends(get_db)):
    db.add(order)
    db.commit()
    db.refresh(order)  # Asegura que la orden esté sincronizada con la base de datos
    return order  # Esto se devolverá como un modelo OrderResponse
