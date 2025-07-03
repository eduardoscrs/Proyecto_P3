# run_fastapi.py
import subprocess
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if not is_port_in_use(8002):
    print("🚀 Iniciando servidor FastAPI en el puerto 8002...")
    subprocess.run(["uvicorn", "Proyect.Api.api:app", "--host", "0.0.0.0", "--port", "8002"])
else:
    print("⚠️ El puerto 8002 ya está en uso. Detén el proceso existente o usa otro puerto.")
