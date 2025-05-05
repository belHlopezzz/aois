import pytest
from table_truth_generator.logical_function import LogicalFunction


def test_logical_function_initialization():
    func = LogicalFunction("x")
    assert func.formula == "x"
    assert func.variables == ["x"]
    assert func.formula_expr == "x"

    func = LogicalFunction("!x")
    assert func.formula == "!x"
    assert func.variables == ["x"]
    assert func.formula_expr == "(not x)"

    func = LogicalFunction("x & y")
    assert func.formula == "x & y"
    assert set(func.variables) == {"x", "y"}
    assert func.formula_expr == "(x and y)"

    func = LogicalFunction("x | y")
    assert func.formula == "x | y"
    assert set(func.variables) == {"x", "y"}
    assert func.formula_expr == "(x or y)"

    func = LogicalFunction("x > y")
    assert func.formula == "x > y"
    assert set(func.variables) == {"x", "y"}
    assert func.formula_expr == "(not x or y)"

    func = LogicalFunction("x ~ y")
    assert func.formula == "x ~ y"
    assert set(func.variables) == {"x", "y"}
    assert func.formula_expr == "(x == y)"


def test_logical_function_evaluation():
    func = LogicalFunction("x")
    assert func.evaluate({"x": True}) is True
    assert func.evaluate({"x": False}) is False

    func = LogicalFunction("!x")
    assert func.evaluate({"x": True}) is False
    assert func.evaluate({"x": False}) is True

    func = LogicalFunction("x & y")
    assert func.evaluate({"x": True, "y": True}) is True
    assert func.evaluate({"x": True, "y": False}) is False
    assert func.evaluate({"x": False, "y": True}) is False
    assert func.evaluate({"x": False, "y": False}) is False

    func = LogicalFunction("x | y")
    assert func.evaluate({"x": True, "y": True}) is True
    assert func.evaluate({"x": True, "y": False}) is True
    assert func.evaluate({"x": False, "y": True}) is True
    assert func.evaluate({"x": False, "y": False}) is False

    func = LogicalFunction("x > y")
    assert func.evaluate({"x": True, "y": True}) is True
    assert func.evaluate({"x": True, "y": False}) is False
    assert func.evaluate({"x": False, "y": True}) is True
    assert func.evaluate({"x": False, "y": False}) is True

    func = LogicalFunction("x ~ y")
    assert func.evaluate({"x": True, "y": True}) is True
    assert func.evaluate({"x": True, "y": False}) is False
    assert func.evaluate({"x": False, "y": True}) is False
    assert func.evaluate({"x": False, "y": False}) is True


def test_complex_expressions():
    func = LogicalFunction("!(x & y) | (z > w) ~ v")
    assert set(func.variables) == {"x", "y", "z", "w", "v"}

    assignment = {"x": True, "y": True, "z": True, "w": True, "v": True}
    assert func.evaluate(assignment) is True

    assignment = {"x": False, "y": False, "z": False, "w": False, "v": False}
    assert func.evaluate(assignment) is False

    assignment = {"x": True, "y": False, "z": True, "w": False, "v": True}
    assert func.evaluate(assignment) is True


def test_nested_parentheses():
    func = LogicalFunction("((x & y) | z) > (a ~ b)")
    assert set(func.variables) == {"x", "y", "z", "a", "b"}

    assignment = {"x": True, "y": True, "z": True, "a": True, "b": True}
    assert func.evaluate(assignment) is True

    assignment = {"x": False, "y": False, "z": False, "a": False, "b": False}
    assert func.evaluate(assignment) is True

    assignment = {"x": True, "y": False, "z": True, "a": False, "b": True}
    assert func.evaluate(assignment) is False


def test_error_handling():
    with pytest.raises(Exception) as exc_info:
        LogicalFunction("x &")
    assert str(exc_info.value) == "Invalid syntax"

    with pytest.raises(Exception) as exc_info:
        LogicalFunction("(x & y")
    assert str(exc_info.value) == "Invalid syntax"

    with pytest.raises(Exception) as exc_info:
        LogicalFunction("x @ y")
    assert str(exc_info.value) == "Invalid character"
