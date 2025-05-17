import pytest
from avl_tree import AVLTree, HashInfo, Node


@pytest.fixture
def avl_tree():
    return AVLTree()


def test_empty_tree(avl_tree):
    assert avl_tree.root is None
    assert avl_tree.collision is False


def test_insert_single_node(avl_tree):
    hash_info = HashInfo("key1", "value1")
    avl_tree.insert(hash_info)
    assert avl_tree.root is not None
    assert avl_tree.root.hash_info.key == "key1"
    assert avl_tree.root.hash_info.value == "value1"
    assert avl_tree.root.height == 1


def test_insert_multiple_nodes(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    assert avl_tree.root is not None
    assert avl_tree.root.hash_info.key == "key2"  # Root should be key2 due to balancing
    assert avl_tree.root.left.hash_info.key == "key1"
    assert avl_tree.root.right.hash_info.key == "key3"


def test_search_existing_node(avl_tree):
    hash_info = HashInfo("key1", "value1")
    avl_tree.insert(hash_info)
    result = avl_tree.search("key1")
    assert result is not None
    assert result.hash_info.key == "key1"
    assert result.hash_info.value == "value1"


def test_search_nonexistent_node(avl_tree):
    hash_info = HashInfo("key1", "value1")
    avl_tree.insert(hash_info)
    result = avl_tree.search("nonexistent")
    assert result is None


def test_delete_leaf_node(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    avl_tree.delete("key1")
    assert avl_tree.search("key1") is None
    assert avl_tree.root is not None
    assert avl_tree.root.hash_info.key == "key2"


def test_delete_node_with_one_child(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    avl_tree.delete("key1")
    assert avl_tree.search("key1") is None
    assert avl_tree.root.hash_info.key == "key2"


def test_delete_node_with_two_children(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
        HashInfo("key4", "value4"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    avl_tree.delete("key2")
    assert avl_tree.search("key2") is None
    assert avl_tree.root is not None


def test_update_existing_node(avl_tree):
    hash_info = HashInfo("key1", "value1")
    avl_tree.insert(hash_info)
    new_hash_info = HashInfo("key1", "new_value")
    avl_tree.update(new_hash_info)
    result = avl_tree.search("key1")
    assert result.hash_info.value == "new_value"


def test_update_nonexistent_node(avl_tree):
    hash_info = HashInfo("key1", "value1")
    avl_tree.insert(hash_info)
    new_hash_info = HashInfo("nonexistent", "new_value")
    avl_tree.update(new_hash_info)
    result = avl_tree.search("nonexistent")
    assert result is None


def test_balance_after_insertion(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
        HashInfo("key4", "value4"),
        HashInfo("key5", "value5"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    assert avl_tree.root is not None
    assert abs(avl_tree._balance_factor(avl_tree.root)) <= 1


def test_balance_after_deletion(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
        HashInfo("key4", "value4"),
        HashInfo("key5", "value5"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    avl_tree.delete("key1")
    avl_tree.delete("key3")

    assert avl_tree.root is not None
    assert abs(avl_tree._balance_factor(avl_tree.root)) <= 1


def test_height_calculation(avl_tree):
    nodes = [
        HashInfo("key1", "value1"),
        HashInfo("key2", "value2"),
        HashInfo("key3", "value3"),
    ]
    for node in nodes:
        avl_tree.insert(node)

    assert avl_tree.root.height == 2
    assert avl_tree.root.left.height == 1
    assert avl_tree.root.right.height == 1


def test_collision_flag(avl_tree):
    assert avl_tree.collision is False
    avl_tree.collision = True
    assert avl_tree.collision is True


def test_hash_info_str_representation():
    hash_info = HashInfo("key1", "value1")
    assert str(hash_info) == "key1 : value1"


def test_node_str_representation():
    hash_info = HashInfo("key1", "value1")
    node = Node(hash_info)
    assert str(node) == "key1 : value1"
