import pytest
from table_truth_generator.language import (
    Token,
    Lexer,
    VARIABLE,
    CONST,
    EQU,
    IMP,
    OR,
    AND,
    NOT,
    LPAREN,
    RPAREN,
    SPACE,
    EOF,
)


def test_token_creation():
    token = Token(VARIABLE, "x")
    assert token.type == VARIABLE
    assert token.value == "x"
    assert str(token) == "Token(VARIABLE, 'x')"
    assert repr(token) == "Token(VARIABLE, 'x')"


def test_lexer_initialization():
    lexer = Lexer("x")
    assert lexer.text == "x"
    assert lexer.pos == 0
    assert lexer.current_char == "x"
    assert lexer.variables == set()

    lexer = Lexer("")
    assert lexer.text == ""
    assert lexer.pos == 0
    assert lexer.current_char is None
    assert lexer.variables == set()


def test_lexer_advance():
    lexer = Lexer("xyz")
    assert lexer.current_char == "x"
    lexer.advance()
    assert lexer.current_char == "y"
    lexer.advance()
    assert lexer.current_char == "z"
    lexer.advance()
    assert lexer.current_char is None


def test_lexer_space_jump():
    lexer = Lexer("   x")
    lexer.space_jump()
    assert lexer.current_char == "x"

    lexer = Lexer("x")
    lexer.space_jump()
    assert lexer.current_char == "x"


def test_lexer_get_variables():
    lexer = Lexer("x & y | z")
    while lexer.get_next_token().type != EOF:
        pass
    assert lexer.get_variables() == ["x", "y", "z"]


def test_lexer_token_recognition():
    lexer = Lexer("x")
    token = lexer.get_next_token()
    assert token.type == VARIABLE
    assert token.value == "x"
    assert lexer.get_next_token().type == EOF

    lexer = Lexer("~")
    token = lexer.get_next_token()
    assert token.type == EQU
    assert token.value == "~"

    lexer = Lexer(">")
    token = lexer.get_next_token()
    assert token.type == IMP
    assert token.value == ">"

    lexer = Lexer("|")
    token = lexer.get_next_token()
    assert token.type == OR
    assert token.value == "|"

    lexer = Lexer("&")
    token = lexer.get_next_token()
    assert token.type == AND
    assert token.value == "&"

    lexer = Lexer("!")
    token = lexer.get_next_token()
    assert token.type == NOT
    assert token.value == "!"

    lexer = Lexer("(")
    token = lexer.get_next_token()
    assert token.type == LPAREN
    assert token.value == "("

    lexer = Lexer(")")
    token = lexer.get_next_token()
    assert token.type == RPAREN
    assert token.value == ")"


def test_lexer_complex_expression():
    lexer = Lexer("(x & y) | !z")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == EOF:
            break

    expected_types = [LPAREN, VARIABLE, AND, VARIABLE, RPAREN, OR, NOT, VARIABLE, EOF]
    assert [t.type for t in tokens] == expected_types
    assert lexer.get_variables() == ["x", "y", "z"]


def test_lexer_error():
    lexer = Lexer("@")
    with pytest.raises(Exception) as exc_info:
        lexer.get_next_token()
    assert str(exc_info.value) == "Invalid character"


def test_lexer_with_spaces():
    lexer = Lexer("x   &   y")
    tokens = []
    while True:
        token = lexer.get_next_token()
        tokens.append(token)
        if token.type == EOF:
            break

    expected_types = [VARIABLE, AND, VARIABLE, EOF]
    assert [t.type for t in tokens] == expected_types
    assert lexer.get_variables() == ["x", "y"]
