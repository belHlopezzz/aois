import pytest
from hash_table import HashTable, BLANK


@pytest.fixture
def hash_table():
    return HashTable(capacity=10)


def test_empty_hash_table(hash_table):
    assert len(hash_table) == 0
    assert hash_table.capacity == 10
    assert all(bucket is BLANK for bucket in hash_table.table)


def test_insert_single_item(hash_table):
    hash_table["key1"] = "value1"
    assert len(hash_table) == 1
    assert hash_table["key1"] == "value1"
    assert "key1" in hash_table


def test_insert_multiple_items(hash_table):
    items = [
        ("key1", "value1"),
        ("key2", "value2"),
        ("key3", "value3"),
    ]
    for key, value in items:
        hash_table[key] = value

    assert len(hash_table) == 3
    for key, value in items:
        assert hash_table[key] == value
        assert key in hash_table


def test_insert_collision(hash_table):
    # Create keys that will collide by using the same characters in different orders
    key1 = "abc"
    key2 = "cba"
    hash_table[key1] = "value1"
    hash_table[key2] = "value2"

    assert len(hash_table) == 2
    assert hash_table[key1] == "value1"
    assert hash_table[key2] == "value2"

    # Check if collision flag is set
    index = hash_table._hash_function(key1)
    assert hash_table.table[index].collision is True


def test_update_existing_item(hash_table):
    hash_table["key1"] = "value1"
    hash_table["key1"] = "new_value"
    assert len(hash_table) == 1
    assert hash_table["key1"] == "new_value"


def test_get_nonexistent_item(hash_table):
    with pytest.raises(KeyError):
        _ = hash_table["nonexistent"]


def test_get_with_default(hash_table):
    assert hash_table.get("nonexistent") is None
    assert hash_table.get("nonexistent", "default") == "default"


def test_delete_existing_item(hash_table):
    hash_table["key1"] = "value1"
    del hash_table["key1"]
    assert len(hash_table) == 0
    assert "key1" not in hash_table


def test_delete_nonexistent_item(hash_table):
    with pytest.raises(KeyError):
        del hash_table["nonexistent"]


def test_delete_collision_item(hash_table):
    key1 = "abc"
    key2 = "cba"
    hash_table[key1] = "value1"
    hash_table[key2] = "value2"

    del hash_table[key1]
    assert len(hash_table) == 1
    assert key1 not in hash_table
    assert hash_table[key2] == "value2"


def test_contains_operator(hash_table):
    hash_table["key1"] = "value1"
    assert "key1" in hash_table
    assert "nonexistent" not in hash_table


def test_string_representation(hash_table):
    hash_table["key1"] = "value1"
    hash_table["key2"] = "value2"

    str_repr = str(hash_table)
    assert "HashTable" in str_repr
    assert "size=10" in str_repr
    assert "items=2" in str_repr


def test_hash_function(hash_table):
    key = "test"
    expected_hash = sum(ord(char) for char in key) % hash_table.capacity
    assert hash_table._hash_function(key) == expected_hash


def test_multiple_collisions(hash_table):
    # Create multiple keys that will collide
    keys = ["abc", "cba", "bac"]
    for i, key in enumerate(keys):
        hash_table[key] = f"value{i}"

    assert len(hash_table) == 3
    for i, key in enumerate(keys):
        assert hash_table[key] == f"value{i}"


def test_delete_last_item_in_bucket(hash_table):
    key1 = "abc"
    key2 = "cba"
    hash_table[key1] = "value1"
    hash_table[key2] = "value2"

    del hash_table[key1]
    del hash_table[key2]

    index = hash_table._hash_function(key1)
    assert hash_table.table[index] is BLANK


def test_print_table(hash_table, capsys):
    hash_table["key1"] = "value1"
    hash_table["key2"] = "value2"
    hash_table.print_table()

    captured = capsys.readouterr()
    assert "HashTable" in captured.out
    assert "Bucket" in captured.out
