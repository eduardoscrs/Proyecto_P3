def serialize_simulation_result(result):
    """
    Convierte el resultado de run_simulation_dynamic a un dict 100% serializable para FastAPI/JSON.
    """
    # Serializar nodos
    def serialize_map(m):
        return {k: v.to_dict() if hasattr(v, 'to_dict') else str(v) for k, v in m.items()}
    def serialize_hashmap(hmap):
        return {k: v.to_dict() if hasattr(v, 'to_dict') else str(v) for k, v in hmap.items()}
    def serialize_avl(avl):
        if hasattr(avl, 'get_top_routes'):
            return avl.get_top_routes(10)
        return str(avl)
    # Serializar nx_graph
    def serialize_nx_graph(nx_graph):
        return {
            'nodes': [
                {'id': n, **nx_graph.nodes[n]} for n in nx_graph.nodes
            ],
            'edges': [
                {'source': u, 'target': v, **d} for u, v, d in nx_graph.edges(data=True)
            ]
        }
    # Serializar storage/client/recharge nodes
    def serialize_list(lst):
        return [str(x) for x in lst]
    return {
        'nx_graph': serialize_nx_graph(result['nx_graph']),
        'orders': [o.to_dict() for o in result['orders']],
        'orders_map': serialize_hashmap(result['orders_map']),
        'storage_nodes': serialize_list(result['storage_nodes']),
        'client_nodes': serialize_list(result['client_nodes']),
        'recharge_nodes': serialize_list(result['recharge_nodes']),
        'clientes': serialize_hashmap(result['clientes']),
        'pedido_avl_root': str(result['pedido_avl_root']),
        'route_avl': serialize_avl(result['route_avl'])
    }
