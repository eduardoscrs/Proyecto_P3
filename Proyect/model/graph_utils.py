from collections import deque
import heapq

def bfs(grafo, start):
    visitados = set()
    cola = deque([start])
    visitados.add(start)

    while cola:
        v = cola.popleft()
        yield v

        for vecino in grafo.vecinos(v):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)


def dijkstra(graph, start_vertex):
    dist = {v: float('inf') for v in graph.vertices()}
    prev = {v: None for v in graph.vertices()}
    dist[start_vertex] = 0

    # Use (distance, vertex_name, vertex) to avoid comparing Vertex objects
    heap = [(0, start_vertex.element(), start_vertex)]

    while heap:
        current_dist, _, current_vertex = heapq.heappop(heap)

        if current_dist > dist[current_vertex]:
            continue

        for neighbor in graph.neighbors(current_vertex):
            edge = graph.get_edge(current_vertex, neighbor)
            weight = edge.element()
            distance = current_dist + weight

            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor.element(), neighbor))

    return dist, prev

def reconstruct_path(prev, start, end):
    path = []
    current = end
    while current != start:
        if current is None:
            return []  # No path found
        path.insert(0, current)
        current = prev[current]
    path.insert(0, start)
    return path

def kruskal_mst(graph):
    """
    Returns a list of edges (u, v) in the MST using Kruskal's algorithm.
    Each edge is represented by the node names (strings).
    """
    parent = dict()
    rank = dict()
    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u
    def union(u, v):
        u_root = find(u)
        v_root = find(v)
        if u_root == v_root:
            return False
        if rank[u_root] < rank[v_root]:
            parent[u_root] = v_root
        else:
            parent[v_root] = u_root
            if rank[u_root] == rank[v_root]:
                rank[u_root] += 1
        return True
    # Inicializar conjuntos
    for v in graph.vertices():
        parent[v] = v
        rank[v] = 0
    # Obtener todas las aristas (u, v, peso)
    edges = []
    for u in graph.vertices():
        for v in graph.neighbors(u):
            edge = graph.get_edge(u, v)
            weight = edge.element()
            # Evitar duplicados en grafo no dirigido
            if (v, u, weight) not in edges:
                edges.append((u, v, weight))
    # Ordenar por peso
    edges.sort(key=lambda x: x[2])
    mst = []
    for u, v, w in edges:
        if union(u, v):
            mst.append((u.element(), v.element()))
    return mst
