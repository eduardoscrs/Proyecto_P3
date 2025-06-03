class Node:
    def __init__(self, key, value=1):  # key es una tupla (ruta), value es la frecuencia
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 0

def height(N):
    return -1 if N is None else N.height

def get_balance(N):
    return 0 if N is None else height(N.left) - height(N.right)

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

def insert(node, key, value=1):
    if node is None:
        return Node(key, value)
    if key < node.key:
        node.left = insert(node.left, key, value)
    elif key > node.key:
        node.right = insert(node.right, key, value)
    else:
        node.value += value  # Incrementar frecuencia si la ruta ya existe
        return node
    node.height = max(height(node.left), height(node.right)) + 1
    balance = get_balance(node)
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

def min_value_node(node):
    current = node
    while current.left:
        current = current.left
    return current

def delete_node(root, key):
    if root is None:
        return root
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None or root.right is None:
            root = root.left or root.right
        else:
            temp = min_value_node(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = delete_node(root.right, temp.key)
    if root is None:
        return root
    root.height = max(height(root.left), height(root.right)) + 1
    balance = get_balance(root)
    if balance > 1 and get_balance(root.left) >= 0:
        return right_rotate(root)
    if balance > 1 and get_balance(root.left) < 0:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and get_balance(root.right) <= 0:
        return left_rotate(root)
    if balance < -1 and get_balance(root.right) > 0:
        root.right = right_rotate(root.right)
        return left_rotate(root)
    return root

def pre_order(root):
    if root:
        print(f"{root.key}: Freq {root.value}", end="; ")
        pre_order(root.left)
        pre_order(root.right)

# Para visualización con networkx
def to_networkx(root, G=None):
    import networkx as nx
    if G is None:
        G = nx.DiGraph()
    if root:
        G.add_node(str(root.key), label=f"{root.key}\nFreq: {root.value}")
        if root.left:
            G.add_edge(str(root.key), str(root.left.key))
            to_networkx(root.left, G)
        if root.right:
            G.add_edge(str(root.key), str(root.right.key))
            to_networkx(root.right, G)
    return G