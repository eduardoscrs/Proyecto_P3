import networkx as nx

def serialize_simulation_result(result):
    """
    Serializa el resultado de la simulación para enviarlo como JSON.
    Convierte el grafo nx a un diccionario serializable.
    """
    def nx_to_dict(graph):
        return {
            "nodes": [
                {"id": n, **graph.nodes[n]} for n in graph.nodes
            ],
            "edges": [
                {"source": u, "target": v, **d} for u, v, d in graph.edges(data=True)
            ]
        }

    return {
        "nx_graph": nx_to_dict(result["nx_graph"]),
        "storage_nodes": result["storage_nodes"],
        "recharge_nodes": result["recharge_nodes"],
        "client_nodes": result["client_nodes"],
        "clientes": {k: v.to_dict() for k, v in result["clientes"].items()},
        "orders": [o.to_dict() for o in result["orders"]],
        "orders_map": {k: o.to_dict() for k, o in result["orders_map"].items()},
        "route_avl": result["route_avl"].to_serializable_dict() if result["route_avl"] else {},
        "graph": None  # No serializamos el grafo personalizado (si tienes uno)
    }
