from abc import abstractmethod, ABC
from typing import Dict, List, Optional

from language import Token

class ExpressionNode(ABC):
    @abstractmethod
    def evaluate(self, assignment: Dict[str, bool], node_values: Optional[Dict['ExpressionNode', bool]] = None) -> bool:
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    @abstractmethod
    def get_nodes_postorder(self) -> List['ExpressionNode']:
        pass


class VariableNode(ExpressionNode):
    def __init__(self, variable: Token):
        self.name = variable.value

    def evaluate(self, assignment: Dict[str, bool], node_values: Optional[Dict['ExpressionNode', bool]] = None) -> bool:
        value = assignment[self.name]
        if node_values is not None:
            node_values[self] = value
        return value

    def to_string(self) -> str:
        return self.name

    def get_nodes_postorder(self) -> List['ExpressionNode']:
        return [self]


class UnaryOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode):
        self.opd = operand
        self.opr = operator
        self.unary_opr = {"NOT": lambda x: not x}

    def evaluate(self, assignment: Dict[str, bool], node_values: Optional[Dict['ExpressionNode', bool]] = None) -> bool:
        opd_value = self.opd.evaluate(assignment, node_values)
        value = self.unary_opr[self.opr.type](opd_value) 
        if node_values is not None:
            node_values[self] = value
        return value

    def to_string(self) -> str:
        return f"{self.opr.value}{self.opd.to_string()}"

    def get_nodes_postorder(self) -> List['ExpressionNode']:
        return self.opd.get_nodes_postorder() + [self]


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

    def evaluate(self, assignment: Dict[str, bool], node_values: Optional[Dict['ExpressionNode', bool]] = None) -> bool:
        left_value = self.left_opd.evaluate(assignment, node_values)
        right_value = self.right_opd.evaluate(assignment, node_values)
        value = self.binary_opr[self.opr.type](left_value, right_value)
        if node_values is not None:
            node_values[self] = value
        return value

    def to_string(self) -> str:
        return f"({self.left_opd.to_string()} {self.opr.value} {self.right_opd.to_string()})"

    def get_nodes_postorder(self) -> List['ExpressionNode']:
        return self.left_opd.get_nodes_postorder() + self.right_opd.get_nodes_postorder() + [self]
