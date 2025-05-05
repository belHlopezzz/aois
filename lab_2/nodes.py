from abc import abstractmethod, ABC
from typing import Dict

from language import Token


class ExpressionNode(ABC):
    @abstractmethod
    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        pass


class VariableNode(ExpressionNode):
    def __init__(self, variable: Token):
        self.name = variable.value

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        return assignment[self.name]


class UnaryOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode):
        self.opd = operand
        self.opr = operator
        self.unary_opr = {"NOT": lambda x: not x}

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        opd_value = self.opd.evaluate(assignment)
        if self.opr.type in self.unary_opr:
            return self.unary_opr[self.opr.type](opd_value)


class BinaryOperationNode(ExpressionNode):
    def __init__(
        self,
        *,
        left_operand: ExpressionNode,
        operator: Token,
        right_operand: ExpressionNode,
    ):
        self.left_opd = left_operand
        self.opr = operator
        self.right_opd = right_operand

        self.binary_opr = {
            "AND": lambda x, y: x and y,
            "OR": lambda x, y: x or y,
            "IMP": lambda x, y: not x or y,
            "EQU": lambda x, y: x == y,
        }

    def evaluate(self, assignment: Dict[str, bool]) -> bool:
        left_opd_value = self.left_opd.evaluate(assignment)
        right_opd_value = self.right_opd.evaluate(assignment)
        if self.opr.type in self.binary_opr:
            return self.binary_opr[self.opr.type](left_opd_value, right_opd_value)
