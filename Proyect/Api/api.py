from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx
from Proyect.sim.simulation import run_simulation_dynamic, dijkstra_shortest_path

# Importar el router con todos los endpoints RESTful
from Proyect.Api.controllers import router as api_router


app = FastAPI()
app.include_router(api_router)  # incluir endpoints combinados

# ============================
# 🚀 SIMULACIÓN Y RUTA DIRECTA
# ============================

class SimulationParams(BaseModel):
    num_nodes: int
    num_edges: int
    num_orders: int

class RouteRequest(BaseModel):
    origen: str
    destino: str

@app.post("/run_simulation/")
async def run_simulation(params: SimulationParams):
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)
    return result

@app.post("/get_route/")
async def get_route(request: RouteRequest):
    nx_graph = run_simulation_dynamic(15, 20, 10)["nx_graph"]  # ejemplo básico
    path = dijkstra_shortest_path(nx_graph, request.origen, request.destino)
    return {"path": path}

@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}
