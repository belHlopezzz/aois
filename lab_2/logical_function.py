from typing import Dict

from language import Lexer
from grammar import Parser

class LogicalFunction:
    def __init__(self, formula: str):
        self.formula = formula
        
        lexer = Lexer(formula)
        parser = Parser(lexer)

        self.ast = parser.parse()
        self.variables = lexer.get_variables()

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        return self.ast.evaluate(assignment)

    def __str__(self):
        return f"LogicalFunction('{self.formula}')"