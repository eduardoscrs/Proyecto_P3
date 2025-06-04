def bfs(grafo, start):
    visitados = set()       # Conjunto para nodos visitados
    cola = [start]          # Cola como lista (FIFO)
    visitados.add(start)    # Marcar el nodo de inicio como visitado

    while cola:             # Mientras la cola no esté vacía
        v = cola.pop(0)     # Sacar el primer elemento (nota: O(n) en listas)
        yield v             # Devolver el nodo visitado

        for vecino in grafo.vecinos(v):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)    


# Ejemplo de uso

if __name__ == "__main__":
    class Grafo:
        def __init__(self):
            self.adjacencias = {}

        def agregar_arista(self, u, v):
            if u not in self.adjacencias:
                self.adjacencias[u] = []
            if v not in self.adjacencias:
                self.adjacencias[v] = []
            self.adjacencias[u].append(v)
            self.adjacencias[v].append(u)

        def vecinos(self, v):
            return self.adjacencias.get(v, [])

    grafo = Grafo()
    grafo.agregar_arista(1, 2)
    grafo.agregar_arista(1, 3)
    grafo.agregar_arista(2, 4)
    grafo.agregar_arista(3, 5)
    grafo.agregar_arista(4, 6)
    grafo.agregar_arista(5, 6)
    grafo.agregar_arista(5, 1)

    for nodo in bfs(grafo, 1):
        print(nodo)

