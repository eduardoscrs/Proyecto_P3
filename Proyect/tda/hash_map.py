class Map:
    def __init__(self, capacity=16):
        self._table = [None] * capacity
        self._size = 0
        self._capacity = capacity

    def _hash(self, key):
        return hash(key) % self._capacity

    def _resize(self):
        old_table = self._table
        self._capacity *= 2
        self._table = [None] * self._capacity
        self._size = 0
        for bucket in old_table:
            if bucket:
                for k, v in bucket:
                    self.put(k, v)

    def put(self, key, value):
        if self._size >= self._capacity * 0.75:
            self._resize()
        index = self._hash(key)
        if self._table[index] is None:
            self._table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self._table[index]):
                if k == key:
                    self._table[index][i] = (key, value)
                    return
            self._table[index].append((key, value))
        self._size += 1

    def get(self, key):
        index = self._hash(key)
        if self._table[index]:
            for k, v in self._table[index]:
                if k == key:
                    return v
        return None

    def remove(self, key):
        index = self._hash(key)
        if self._table[index]:
            for i, (k, v) in enumerate(self._table[index]):
                if k == key:
                    self._table[index].pop(i)
                    self._size -= 1
                    return v
        return None

    def __len__(self):
        return self._size