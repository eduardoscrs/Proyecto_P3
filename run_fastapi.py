import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("Proyect.Api.api:app", host="0.0.0.0", port=8002, reload=True)
