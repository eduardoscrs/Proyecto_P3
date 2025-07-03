import socket
import subprocess
import os
import sys
import time

# Asegura que los imports funcionen
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_fastapi_once():
    """Inicia FastAPI solo si aún no ha sido lanzado y el puerto está libre."""
    if os.environ.get("FASTAPI_STARTED") != "1":
        os.environ["FASTAPI_STARTED"] = "1"
        if not is_port_in_use(8002):
            print("🔄 Iniciando FastAPI en http://localhost:8002 ...")
            subprocess.Popen(["uvicorn", "Proyect.Api.api:app", "--host", "0.0.0.0", "--port", "8002"])
            time.sleep(1.5)
        else:
            print("⚠️ El puerto 8002 ya está en uso.")
    else:
        print("⚠️ FastAPI ya está activo (FASTAPI_STARTED=1).")

# Ejecutar automáticamente al lanzar con streamlit
start_fastapi_once()

# Importa el dashboard de Streamlit y lo ejecuta
from Proyect.visual.dashboard import main as streamlit_main
streamlit_main()
