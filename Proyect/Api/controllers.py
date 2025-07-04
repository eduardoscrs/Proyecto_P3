from fastapi import APIRouter

router = APIRouter()

@router.get("/clientes")
def get_clientes():
    return {"msg": "Lista de clientes"}
