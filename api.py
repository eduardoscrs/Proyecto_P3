# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from Proyect.visual.dashboard import run_simulation_dynamic

app = FastAPI()

# Definir modelo para los parámetros de la simulación
class SimulationParams(BaseModel):
    num_nodes: int
    num_edges: int
    num_orders: int

@app.post("/run_simulation/")
async def run_simulation(params: SimulationParams):
    result = run_simulation_dynamic(params.num_nodes, params.num_edges, params.num_orders)
    return result

@app.get("/status/")
async def get_status():
    return {"status": "API is running", "message": "Use POST to start a simulation"}
