class Node:
    def __init__(self, key, value=1):  # key puede ser una ruta, value su frecuencia
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    return node.height if node else 0


def get_balance(node):
    return height(node.left) - height(node.right) if node else 0


def right_rotate(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    y.height = max(height(y.left), height(y.right)) + 1
    x.height = max(height(x.left), height(x.right)) + 1

    return x


def left_rotate(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    x.height = max(height(x.left), height(x.right)) + 1
    y.height = max(height(y.left), height(y.right)) + 1

    return y


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value=1):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value += value
            return node

        node.height = 1 + max(height(node.left), height(node.right))
        balance = get_balance(node)

        # Casos de desbalanceo
        if balance > 1 and key < node.left.key:
            return right_rotate(node)
        if balance < -1 and key > node.right.key:
            return left_rotate(node)
        if balance > 1 and key > node.left.key:
            node.left = left_rotate(node.left)
            return right_rotate(node)
        if balance < -1 and key < node.right.key:
            node.right = right_rotate(node.right)
            return left_rotate(node)

        return node

    def get_top_routes(self, k=5):
        result = []
        self._inorder_collect(self.root, result)
        result.sort(key=lambda x: x[1], reverse=True)  # ordenar por frecuencia
        return result[:k]

    def _inorder_collect(self, node, result):
        if not node:
            return
        self._inorder_collect(node.left, result)
        result.append((node.key, node.value))
        self._inorder_collect(node.right, result)

    def to_networkx(self):
        import networkx as nx
        G = nx.DiGraph()
        self._build_graph(self.root, G)
        return G

    def _build_graph(self, node, G):
        if not node:
            return
        G.add_node(str(node.key), label=f"{node.key}\nFreq: {node.value}")
        if node.left:
            G.add_edge(str(node.key), str(node.left.key))
            self._build_graph(node.left, G)
        if node.right:
            G.add_edge(str(node.key), str(node.right.key))
            self._build_graph(node.right, G)
