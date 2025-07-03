from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import networkx as nx

# Simulación
from Proyect.sim.simulation import run_simulation_dynamic, dijkstra_shortest_path
from Proyect.sim.serialize_utils import serialize_simulation_result

# Base de datos
from Proyect.data.dependencies import get_db
from Proyect.data.models import Client, Order

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
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)

    # Guardar CLIENTES
    for client_id, client_obj in result["clientes"].items():
        db_client = Client(id=client_id, name=client_obj.nombre, total_orders=client_obj.total_orders)
        db.merge(db_client)

    # Guardar ÓRDENES con estado
    for order in result["orders"]:
        status = "delivered" if getattr(order, "estado", "").lower() == "entregada" else "pending"
        db_order = Order(id=order.id, origen=order.origen, destino=order.destino, status=status)
        db.merge(db_order)

    db.commit()
    return serialize_simulation_result(result)

@app.post("/get_route/")
async def get_route(request: RouteRequest):
    sim = run_simulation_dynamic(15, 20, 10)  # temporal
    nx_graph = sim["nx_graph"]
    path = dijkstra_shortest_path(nx_graph, request.origen, request.destino)
    return {"path": path}

@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}
