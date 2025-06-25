# app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Proyect.visual.dashboard import main
import uvicorn
from api import app  # Importar la API

if __name__ == "__main__":
    # Iniciar el servidor FastAPI en segundo plano
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # También puedes arrancar el frontend de Streamlit si lo necesitas
    main()
