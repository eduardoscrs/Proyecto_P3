from collections import deque

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
