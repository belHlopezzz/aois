from src.avl_tree import AVLTree, HashInfo
from utils.tree_printer import print_tree

BLANK = object()


class HashTable:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.length = 0
        self.table = [BLANK] * capacity

    def __len__(self):
        return self.length

    def __setitem__(self, key, value):
        index = self._hash_function(key)
        hash_info = HashInfo(key, value)
        if self.table[index] is BLANK:
            self.table[index] = AVLTree()
        elif self.table[index].root is not None:
            self.table[index].collision = True

        if key not in self:
            self.table[index].insert(hash_info)
            self.length += 1
        else:
            self.table[index].update(hash_info)

    def __getitem__(self, key):
        index = self._hash_function(key)
        if self.table[index] is BLANK:
            raise KeyError(key)
        node = self.table[index].search(key)
        if node is None:
            raise KeyError(key)
        return node.hash_info.value

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __delitem__(self, key):
        index = self._hash_function(key)
        if self.table[index] is BLANK:
            raise KeyError(key)
        node = self.table[index].search(key)
        if node is None:
            raise KeyError(key)
        else:
            self.table[index].delete(key)
            self.length -= 1
            if self.table[index].root is None:
                self.table[index] = BLANK

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def _hash_function(self, key):
        return sum(ord(char) for char in key) % self.capacity

    def __str__(self):
        result = []
        result.append(f"HashTable(size={self.capacity}, items={self.length})")

        for i, tree in enumerate(self.table):
            if tree is not BLANK:
                result.append(
                    f"Bucket {i}: {tree.collision and 'Has collisions' or 'No collisions'}"
                )

        return "\n".join(result)

    def __repr__(self):
        return self.__str__()

    def print_table(self):
        print(f"HashTable(size={self.capacity}, items={self.length})")
        for i, tree in enumerate(self.table):
            if tree is not BLANK:
                print(f"Bucket {i}:")
                tree.print_tree()
                print()
