from utils.tree_printer import print_tree


class HashInfo:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"{self.key} : {self.value}"


class Node:
    def __init__(self, hash_info: HashInfo):
        self.hash_info = hash_info
        self.left = None
        self.right = None
        self.height = 1


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

    def insert(self, root, hash_info: HashInfo):
        if not root:
            return Node(hash_info)
        elif hash_info.key < root.hash_info.key:
            root.left = self.insert(root.left, hash_info)
        else:
            root.right = self.insert(root.right, hash_info)

        root.height = 1 + max(self._height(root.left), self._height(root.right))

        balance = self._balance_factor(root)

        if balance > 1:
            if hash_info.key < root.left.hash_info.key:
                return self._rotate_right(root)
            else:
                root.left = self._rotate_left(root.left)
                return self._rotate_right(root)
        if balance < -1:
            if hash_info.key > root.right.hash_info.key:
                return self._rotate_left(root)
            else:
                root.right = self._rotate_right(root.right)
                return self._rotate_left(root)

        return root

    def _min_value_node(self, node):
        current = node
        while current and current.left:
            current = current.left
        return current

    def delete(self, root, key):
        if not root:
            return root

        if key < root.hash_info.key:
            root.left = self.delete(root.left, key)
        elif key > root.hash_info.key:
            root.right = self.delete(root.right, key)
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
            root.right = self.delete(root.right, temp.hash_info.key)

        root.height = 1 + max(self._height(root.left), self._height(root.right))

        balance = self._balance_factor(root)

        if balance > 1:
            if self._balance_factor(root.left) >= 0:
                return self._rotate_right(root)
            else:
                root.left = self._rotate_left(root.left)
                return self._rotate_right(root)
        elif balance < -1:
            if self._balance_factor(root.right) <= 0:
                return self._rotate_left(root)
            else:
                root.right = self._rotate_right(root.right)
                return self._rotate_left(root)

        return root


def main():
    avl = AVLTree()
    keys = ["Война и мир", "Евгений Онегин", "Преступление и наказание", "Мертвые души", 
            "Мастер и Маргарита", "Идиот", "Отцы и дети", "Герой нашего времени",
            "Анна Каренина", "Капитанская дочка", "Ревизор", "Вишневый сад", "Обломов"]
    values = ["Толстой", "Пушкин", "Достоевский", "Гоголь",
              "Булгаков", "Достоевский", "Тургенев", "Лермонтов", 
              "Толстой", "Пушкин", "Гоголь", "Чехов", "Гончаров"]

    for key, value in zip(keys, values):
        avl.root = avl.insert(avl.root, HashInfo(key, value))

    print_tree(avl.root)


if __name__ == "__main__":
    main()
