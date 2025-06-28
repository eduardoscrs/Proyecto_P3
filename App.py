import sys
import os
import subprocess
from Proyect.visual.dashboard import main
import uvicorn
from api import app  # Importar la API

if __name__ == "__main__":
    # Iniciar el servidor FastAPI en segundo plano usando subprocess
    uvicorn_process = subprocess.Popen(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])

    # Iniciar el frontend de Streamlit en segundo plano
    streamlit_process = subprocess.Popen(["streamlit", "run", "app.py"])

    # Esperar a que ambos procesos terminen
    uvicorn_process.wait()
    streamlit_process.wait()
