import pytest
from table_truth_generator.language import Token, VARIABLE, NOT, AND, OR, IMP, EQU
from table_truth_generator.nodes import (
    VariableNode,
    UnaryOperationNode,
    BinaryOperationNode,
)


def test_variable_node():
    token = Token(VARIABLE, "x")
    node = VariableNode(token)
    assert node.name == "x"
    assert node.to_python() == "x"


def test_unary_operation_node():
    var_token = Token(VARIABLE, "x")
    not_token = Token(NOT, "!")
    var_node = VariableNode(var_token)
    not_node = UnaryOperationNode(not_token, var_node)

    assert not_node.to_python() == "(not x)"

    unknown_token = Token("UNKNOWN", "?")
    unknown_node = UnaryOperationNode(unknown_token, var_node)
    with pytest.raises(ValueError) as exc_info:
        unknown_node.to_python()
    assert str(exc_info.value) == "Unknown unary operator"


def test_binary_operation_node():
    x_token = Token(VARIABLE, "x")
    y_token = Token(VARIABLE, "y")
    x_node = VariableNode(x_token)
    y_node = VariableNode(y_token)

    and_token = Token(AND, "&")
    and_node = BinaryOperationNode(
        left_operand=x_node, operator=and_token, right_operand=y_node
    )
    assert and_node.to_python() == "(x and y)"

    or_token = Token(OR, "|")
    or_node = BinaryOperationNode(
        left_operand=x_node, operator=or_token, right_operand=y_node
    )
    assert or_node.to_python() == "(x or y)"

    imp_token = Token(IMP, ">")
    imp_node = BinaryOperationNode(
        left_operand=x_node, operator=imp_token, right_operand=y_node
    )
    assert imp_node.to_python() == "(not x or y)"

    equ_token = Token(EQU, "~")
    equ_node = BinaryOperationNode(
        left_operand=x_node, operator=equ_token, right_operand=y_node
    )
    assert equ_node.to_python() == "(x == y)"

    unknown_token = Token("UNKNOWN", "?")
    unknown_node = BinaryOperationNode(
        left_operand=x_node, operator=unknown_token, right_operand=y_node
    )
    with pytest.raises(ValueError) as exc_info:
        unknown_node.to_python()
    assert str(exc_info.value) == "Unknown binary operator"


def test_nested_operations():
    x_token = Token(VARIABLE, "x")
    y_token = Token(VARIABLE, "y")
    z_token = Token(VARIABLE, "z")

    x_node = VariableNode(x_token)
    y_node = VariableNode(y_token)
    z_node = VariableNode(z_token)

    and_token = Token(AND, "&")
    and_node = BinaryOperationNode(
        left_operand=x_node, operator=and_token, right_operand=y_node
    )

    not_token = Token(NOT, "!")
    not_node = UnaryOperationNode(not_token, and_node)

    or_token = Token(OR, "|")
    final_node = BinaryOperationNode(
        left_operand=not_node, operator=or_token, right_operand=z_node
    )

    assert final_node.to_python() == "((not (x and y)) or z)"
