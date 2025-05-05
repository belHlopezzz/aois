import pytest
from table_truth_generator.language import (
    Lexer,
    VARIABLE,
    NOT,
    AND,
    OR,
    LPAREN,
    RPAREN,
    IMP,
    EQU,
    EOF,
)
from table_truth_generator.grammar import Parser


def test_parser_initialization():
    lexer = Lexer("x")
    parser = Parser(lexer)
    assert parser.lexer == lexer
    assert parser.current_token.type == VARIABLE
    assert parser.current_token.value == "x"


def test_parser_eat():
    lexer = Lexer("x & y")
    parser = Parser(lexer)

    parser.eat(VARIABLE)
    assert parser.current_token.type == AND

    with pytest.raises(Exception) as exc_info:
        parser.eat(VARIABLE)
    assert str(exc_info.value) == "Invalid syntax"


def test_parser_element():
    lexer = Lexer("x")
    parser = Parser(lexer)
    node = parser.element()
    assert node.name == "x"
    assert parser.current_token.type == EOF

    lexer = Lexer("!x")
    parser = Parser(lexer)
    node = parser.element()
    assert node.to_python() == "(not x)"
    assert parser.current_token.type == EOF

    lexer = Lexer("(x & y)")
    parser = Parser(lexer)
    node = parser.element()
    assert node.to_python() == "(x and y)"
    assert parser.current_token.type == EOF

    lexer = Lexer("&")
    parser = Parser(lexer)
    with pytest.raises(Exception) as exc_info:
        parser.element()
    assert str(exc_info.value) == "Invalid syntax"


def test_parser_conjunction():
    lexer = Lexer("x")
    parser = Parser(lexer)
    node = parser.conjunction()
    assert node.to_python() == "x"

    lexer = Lexer("x & y")
    parser = Parser(lexer)
    node = parser.conjunction()
    assert node.to_python() == "(x and y)"

    lexer = Lexer("x & y & z")
    parser = Parser(lexer)
    node = parser.conjunction()
    assert node.to_python() == "((x and y) and z)"


def test_parser_disjunction():
    lexer = Lexer("x")
    parser = Parser(lexer)
    node = parser.disjunction()
    assert node.to_python() == "x"

    lexer = Lexer("x | y")
    parser = Parser(lexer)
    node = parser.disjunction()
    assert node.to_python() == "(x or y)"

    lexer = Lexer("x | y | z")
    parser = Parser(lexer)
    node = parser.disjunction()
    assert node.to_python() == "((x or y) or z)"


def test_parser_implication():
    lexer = Lexer("x")
    parser = Parser(lexer)
    node = parser.implication()
    assert node.to_python() == "x"

    lexer = Lexer("x > y")
    parser = Parser(lexer)
    node = parser.implication()
    assert node.to_python() == "(not x or y)"

    lexer = Lexer("x > y > z")
    parser = Parser(lexer)
    node = parser.implication()
    assert node.to_python() == "(not (not x or y) or z)"


def test_parser_equivalence():
    lexer = Lexer("x")
    parser = Parser(lexer)
    node = parser.equivalence()
    assert node.to_python() == "x"

    lexer = Lexer("x ~ y")
    parser = Parser(lexer)
    node = parser.equivalence()
    assert node.to_python() == "(x == y)"

    lexer = Lexer("x ~ y ~ z")
    parser = Parser(lexer)
    node = parser.equivalence()
    assert node.to_python() == "((x == y) == z)"


def test_parser_complex_expressions():
    lexer = Lexer("!(x & y) | (z > w) ~ v")
    parser = Parser(lexer)
    node = parser.parse()
    assert node.to_python() == "(((not (x and y)) or (not z or w)) == v)"

    lexer = Lexer("((x & y) | z) > (a ~ b)")
    parser = Parser(lexer)
    node = parser.parse()
    assert node.to_python() == "(not ((x and y) or z) or (a == b))"


def test_parser_error_handling():
    lexer = Lexer("(x & y")
    parser = Parser(lexer)
    with pytest.raises(Exception) as exc_info:
        parser.parse()
    assert str(exc_info.value) == "Invalid syntax"

    lexer = Lexer("x & y &")
    parser = Parser(lexer)
    with pytest.raises(Exception) as exc_info:
        parser.parse()
    assert str(exc_info.value) == "Invalid syntax"

    lexer = Lexer("& x")
    parser = Parser(lexer)
    with pytest.raises(Exception) as exc_info:
        parser.parse()
    assert str(exc_info.value) == "Invalid syntax"
