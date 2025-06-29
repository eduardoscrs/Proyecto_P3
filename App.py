import sys
import os
import subprocess

from Proyect.visual.dashboard import main
from Proyect.Api.api import app  

if __name__ == "__main__":
    # Iniciar el servidor FastAPI en segundo plano usando la ruta correcta
    uvicorn_process = subprocess.Popen(["uvicorn", "Proyect.Api.api:app", "--host", "0.0.0.0", "--port", "8002"])

    # Iniciar el frontend de Streamlit
    streamlit_process = subprocess.Popen(["streamlit", "run", "App.py"])

    # Esperar a que ambos procesos terminen
    uvicorn_process.wait()
    streamlit_process.wait()
