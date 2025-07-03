# run_dashboard.py
import subprocess
import os
import sys

# Ruta absoluta al directorio raíz del proyecto (donde está Proyect/)
project_root = os.path.abspath(os.path.dirname(__file__))

# Establece la variable de entorno PYTHONPATH
env = os.environ.copy()
env["PYTHONPATH"] = project_root

print("🖥️ Iniciando el dashboard de Streamlit...")
subprocess.run(["streamlit", "run", "Proyect/visual/dashboard.py"], env=env)
