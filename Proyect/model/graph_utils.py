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

    heap = [(0, start_vertex)]

    while heap:
        current_dist, current_vertex = heapq.heappop(heap)

        if current_dist > dist[current_vertex]:
            continue

        for neighbor in graph.neighbors(current_vertex):
            edge = graph.get_edge(current_vertex, neighbor)
            weight = edge.element()
            distance = current_dist + weight

            if distance < dist[neighbor]:
                dist[neighbor] = distance
                prev[neighbor] = current_vertex
                heapq.heappush(heap, (distance, neighbor))

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
