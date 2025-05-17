from PrettyPrint import PrettyPrintTree


def print_tree(root):
    if not root:
        print("Tree is empty")
        return

    printer = PrettyPrintTree(
        lambda node: [node.left, node.right] if node else [],
        lambda node: node.hash_info if node else None,
        orientation=PrettyPrintTree.Horizontal
    )
    printer(root)
