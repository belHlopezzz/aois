from typing import Set, List

VARIABLE, CONST, EQU, IMP, OR, AND, NOT, LPAREN, RPAREN, SPACE, EOF = (
    "VARIABLE",
    "CONST",
    "EQU",
    "IMP",
    "OR",
    "AND",
    "NOT",
    "LPAREN",
    "RPAREN",
    "SPACE",
    "EOF",
)


class Token:
    def __init__(self, type: str, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None      
        self.variables: Set[str] = set()

    def error(self):
        raise Exception("Invalid character")
    
    def get_variables(self) -> List[str]:
        return sorted(list(self.variables))

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def space_jump(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self) -> Token:
        # Lexical analyzer
        while self.current_char is not None:
            if self.current_char.isspace():
                self.space_jump()
                continue

            if self.current_char.isalpha():
                self.variables.add(self.current_char)
                char = self.current_char
                self.advance()
                return Token(VARIABLE, char)

            if self.current_char == "~":
                self.advance()
                return Token(EQU, "~")

            if self.current_char == ">":
                self.advance()
                return Token(IMP, ">")

            if self.current_char == "|":
                self.advance()
                return Token(OR, "|")

            if self.current_char == "&":
                self.advance()
                return Token(AND, "&")

            if self.current_char == "!":
                self.advance()
                return Token(NOT, "!")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)