# App.py en raíz del proyecto
import subprocess
import socket
import os
import sys

# Asegura que los imports funcionen
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importa la API de FastAPI y el dashboard de Streamlit
from Proyect.Api.api import app as fastapi_app
from Proyect.visual.dashboard import main as streamlit_main

def is_port_in_use(port):
    """Verifica si un puerto ya está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run():
    # Lanza FastAPI en segundo plano si el puerto está libre
    if not is_port_in_use(8002):
        print("🔄 Iniciando servidor FastAPI en el puerto 8002...")
        subprocess.Popen(["uvicorn", "Proyect.Api.api:app", "--host", "0.0.0.0", "--port", "8002"])
    else:
        print("⚠️ El puerto 8002 ya está en uso. FastAPI no se iniciará nuevamente.")

    # Inicia la interfaz Streamlit
    print("🚀 Abriendo el dashboard de Streamlit...")
    streamlit_main()

if __name__ == "__main__":
    run()
