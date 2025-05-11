from abc import abstractmethod, ABC

from src.pnf_contructor.language import Token


class ExpressionNode(ABC):
    @abstractmethod
    def to_python(self):
        pass


class VariableNode(ExpressionNode):
    def __init__(self, variable: Token):
        self.name = variable.value

    def to_python(self) -> str:
        return self.name


class UnaryOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode):
        self.opd = operand
        self.opr = operator
        self.unary_opr = {"NOT": lambda x: f"(not {x})"}

    def to_python(self) -> str:
        opd_value = self.opd.to_python()
        if self.opr.type in self.unary_opr:
            return self.unary_opr[self.opr.type](opd_value)
        else:
            raise ValueError("Unknown unary operator")


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
            "AND": lambda x, y: f"({x} and {y})",
            "OR": lambda x, y: f"({x} or {y})",
            "IMP": lambda x, y: f"(not {x} or {y})",
            "EQU": lambda x, y: f"({x} == {y})",
        }

    def to_python(self) -> str:
        left_opd_value = self.left_opd.to_python()
        right_opd_value = self.right_opd.to_python()
        if self.opr.type in self.binary_opr:
            return self.binary_opr[self.opr.type](left_opd_value, right_opd_value)
        else:
            raise ValueError("Unknown binary operator")
