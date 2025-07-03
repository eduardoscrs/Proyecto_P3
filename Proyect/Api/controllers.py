
from fastapi import APIRouter, HTTPException, Response
from typing import List
from Proyect.domain.client import Client
from Proyect.domain.order import Order

router = APIRouter()

# ==========================
# 📦 CLIENT ENDPOINTS
# ==========================
clientes_simulados = {}  # clave: client_id -> Client

@router.get("/clients/")
def get_all_clients():
    return [c.to_dict() for c in clientes_simulados.values()]

@router.get("/clients/{client_id}")
def get_client_by_id(client_id: str):
    client = clientes_simulados.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client.to_dict()

# ==========================
# 📦 ORDER ENDPOINTS
# ==========================
ordenes_simuladas = {}  # clave: order_id -> Order

@router.get("/orders/")
def get_all_orders():
    return [o.to_dict() for o in ordenes_simuladas.values()]

@router.get("/orders/orders/{order_id}")
def get_order(order_id: str):
    order = ordenes_simuladas.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()

@router.post("/orders/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    order = ordenes_simuladas.get(order_id)
    if not order or order.status == "completed":
        raise HTTPException(status_code=400, detail="Order not cancelable")
    order.status = "cancelled"
    return {"status": "cancelled", "order_id": order_id}

@router.post("/orders/orders/{order_id}/complete")
def complete_order(order_id: str):
    order = ordenes_simuladas.get(order_id)
    if not order or order.status != "pending":
        raise HTTPException(status_code=400, detail="Order not completable")
    order.status = "completed"
    return {"status": "completed", "order_id": order_id}

# ==========================
# 📄 REPORT ENDPOINT
# ==========================
@router.get("/reports/reports/pdf")
def download_report_pdf():
    sample_pdf = b"%PDF-1.4\n%..."  # simulado
    return Response(content=sample_pdf, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=reporte_simulacion.pdf"
    })

# ==========================
# 📊 INFO REPORTS ENDPOINTS
# ==========================
@router.get("/info/reports/visits/clients")
def top_clients():
    return [{"client_id": "A", "visits": 12}, {"client_id": "B", "visits": 8}]

@router.get("/info/reports/visits/recharges")
def top_recharges():
    return [{"node": "R1", "visits": 14}]

@router.get("/info/reports/visits/storages")
def top_storages():
    return [{"node": "S1", "visits": 9}]

@router.get("/info/reports/summary")
def global_summary():
    return {
        "total_clients": 10,
        "total_orders": 25,
        "total_deliveries": 18
    }
