from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import networkx as nx
from sqlalchemy.orm import Session

# Importaciones de simulación y serialización
from Proyect.sim.simulation import run_simulation_dynamic, dijkstra_shortest_path
<<<<<<< Updated upstream
=======
from Proyect.sim.serialize_utils import serialize_simulation_result

# Importaciones de base de datos
from Proyect.data.dependencies import get_db
from Proyect.data import crud, models

# Importar el router modular (clientes, órdenes, etc.)
from Proyect.Api.controllers import router as api_router
>>>>>>> Stashed changes

# Inicializar FastAPI
app = FastAPI(
    title="Drone Logistics API",
    version="1.0",
    description="API para simulación logística y gestión de pedidos/clientes"
)

<<<<<<< Updated upstream
app = FastAPI()
=======
# Incluir router externo con endpoints RESTful
app.include_router(api_router)

# =============================
# 🚀 SIMULACIÓN Y RUTAS
# =============================
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    # Ejecutar la simulación con los parámetros proporcionados
=======
    """Ejecuta una simulación dinámica"""
>>>>>>> Stashed changes
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)
    return result

# Endpoint para obtener una ruta entre nodos usando Dijkstra
@app.post("/get_route/")
async def get_route(request: RouteRequest):
<<<<<<< Updated upstream
    # Cargar el grafo de la simulación
    nx_graph = run_simulation_dynamic(15, 20, 10)["nx_graph"]  # ejemplo de simulación
=======
    """Obtiene la ruta óptima entre nodos usando Dijkstra"""
    nx_graph = run_simulation_dynamic(15, 20, 10)["nx_graph"]  # simulación de ejemplo
>>>>>>> Stashed changes
    path = dijkstra_shortest_path(nx_graph, request.origen, request.destino)
    return {"path": path}

# Endpoint para verificar el estado de la API
@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}
