from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx
from Proyect.sim.simulation import run_simulation_dynamic, dijkstra_shortest_path


app = FastAPI()

# Definir modelo para los parámetros de la simulación
class SimulationParams(BaseModel):
    num_nodes: int
    num_edges: int
    num_orders: int

class RouteRequest(BaseModel):
    origen: str
    destino: str
# Endpoint para ejecutar la simulación
@app.post("/run_simulation/")
async def run_simulation(params: SimulationParams):
    # Ejecutar la simulación con los parámetros proporcionados
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)
    return result

# Endpoint para obtener una ruta entre nodos usando Dijkstra
@app.post("/get_route/")
async def get_route(request: RouteRequest):
    # Cargar el grafo de la simulación
    nx_graph = run_simulation_dynamic(15, 20, 10)["nx_graph"]  # ejemplo de simulación
    path = dijkstra_shortest_path(nx_graph, request.origen, request.destino)
    return {"path": path}

# Endpoint para verificar el estado de la API
@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}
