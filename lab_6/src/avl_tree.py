from utils.tree_printer import print_tree


class HashInfo:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key} : {self.value}"


class Node:
    def __init__(self, hash_info: HashInfo):
        self.hash_info = hash_info
        self.left = None
        self.right = None
        self.height = 1

    def __str__(self):
        return str(self.hash_info)


class AVLTree:
    def __init__(self):
        self.root = None
        self.collision = False

    def _height(self, node):
        if not node:
            return 0
        return node.height

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _balance_factor(self, node):
        """Calculate balance factor of a node (left height - right height)"""
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def search(self, key):
        x = self.root
        while x is not None and key != x.hash_info.key:
            if key < x.hash_info.key:
                x = x.left
            else:
                x = x.right
        return x

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def insert(self, hash_info: HashInfo):
        self.root = self._insert(self.root, hash_info)

    def _insert(self, root, hash_info: HashInfo):
        if not root:
            return Node(hash_info)
        elif hash_info.key < root.hash_info.key:
            root.left = self._insert(root.left, hash_info)
        else:
            root.right = self._insert(root.right, hash_info)

        root.height = 1 + max(self._height(root.left), self._height(root.right))

        balance = self._balance_factor(root)

        # 4. If unbalanced, perform rotations
        # Left-Left Case
        if balance > 1 and hash_info.key < root.left.hash_info.key:
            return self._rotate_right(root)

        # Right-Right Case
        if balance < -1 and hash_info.key > root.right.hash_info.key:
            return self._rotate_left(root)

        # Left-Right Case
        if balance > 1 and hash_info.key > root.left.hash_info.key:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Right-Left Case
        if balance < -1 and hash_info.key < root.right.hash_info.key:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def _min_value_node(self, node):
        """Find node with minimum key value in the tree rooted at node"""
        current = node
        while current and current.left:
            current = current.left
        return current

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if not root:
            return root

        if key < root.hash_info.key:
            root.left = self._delete(root.left, key)
        elif key > root.hash_info.key:
            root.right = self._delete(root.right, key)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self._min_value_node(root.right)
            root.hash_info = HashInfo(temp.hash_info.key, temp.hash_info.value)
            root.right = self._delete(root.right, temp.hash_info.key)

        root.height = 1 + max(self._height(root.left), self._height(root.right))

        balance = self._balance_factor(root)

        # 4. Rebalance if needed
        # Left-Left Case
        if balance > 1 and self._balance_factor(root.left) >= 0:
            return self._rotate_right(root)

        # Left-Right Case
        if balance > 1 and self._balance_factor(root.left) < 0:
            root.left = self._rotate_left(root.left)
            return self._rotate_right(root)

        # Right-Right Case
        if balance < -1 and self._balance_factor(root.right) <= 0:
            return self._rotate_left(root)

        # Right-Left Case
        if balance < -1 and self._balance_factor(root.right) > 0:
            root.right = self._rotate_right(root.right)
            return self._rotate_left(root)

        return root

    def update(self, new_hash_info: HashInfo):
        """Update the value of an existing key"""
        node = self.search(new_hash_info.key)
        if node is not None:
            node.hash_info.value = new_hash_info.value

    def print_tree(self):
        print_tree(self.root)
