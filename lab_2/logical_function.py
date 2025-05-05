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

        self.formula_expr = self.ast.to_python()
        var_list = ", ".join(self.variables)
        self.eval_formula = eval(f"lambda {var_list}: {self.formula_expr}")

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        # if set(assignment.keys()) != set(self.variables):
        #     raise ValueError("Assignment must include all variables")
        return self.eval_formula(**assignment)
