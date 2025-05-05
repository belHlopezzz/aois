from typing import List, Dict
import itertools
from tabulate import tabulate

from logical_function import LogicalFunction
from nodes import UnaryOperationNode, BinaryOperationNode, VariableNode, ExpressionNode


class TruthTable:
    def __init__(self, logical_function: LogicalFunction):
        self.logical_function = logical_function
        self.variables = logical_function.variables
        self.nodes = logical_function.ast.get_nodes_postorder()
        self.node_strings = [node.to_string() for node in self.nodes]
        self.table = self._build_table()

    def _build_table(self) -> List[Dict[str, bool]]:
        table = []
        assignments = list(
            itertools.product([False, True], repeat=len(self.variables))
        )
        for assignment in assignments:
            assignment_dict = dict(zip(self.variables, assignment))
            node_values = {}
            self.logical_function.ast.evaluate(assignment_dict, node_values)
            row = {var: assignment_dict[var] for var in self.variables}
            for node, node_str in zip(self.nodes, self.node_strings):
                row[node_str] = node_values[node]
            table.append(row)
        return table

    def display(self):
        if not self.table:
            print("Таблица истинности не сгенерирована.")
            return

        operator_nodes = [
            node
            for node in self.nodes
            if isinstance(node, (UnaryOperationNode, BinaryOperationNode))
        ]
        operator_display_names = [node.to_string() for node in operator_nodes]
        all_columns = self.variables + operator_display_names

        table_data = []
        for row in self.table:
            row_data = [int(row[col]) for col in all_columns]
            table_data.append(row_data)

        print(tabulate(table_data, headers=all_columns, tablefmt="simple_grid"))

    def get_dnf(self) -> str:
        root_str = self.node_strings[-1]
        true_rows = [row for row in self.table if row[root_str]]
        if not true_rows:
            return "0"
        terms = []
        for row in true_rows:
            term = " & ".join(
                [var if row[var] else f"!{var}" for var in self.variables]
            )
            terms.append(term)
        return " | ".join([f"({term})" for term in terms])

    def get_cnf(self) -> str:
        root_str = self.node_strings[-1]
        false_rows = [row for row in self.table if not row[root_str]]
        if not false_rows:
            return "1"
        terms = []
        for row in false_rows:
            term = " | ".join(
                [f"!{var}" if row[var] else var for var in self.variables]
            )
            terms.append(term)
        return " & ".join([f"({term})" for term in terms])

    def get_dnf_indices(self) -> List[int]:
        root_str = self.node_strings[-1]
        return [i for i, row in enumerate(self.table) if row[root_str]]

    def get_cnf_indices(self) -> List[int]:
        root_str = self.node_strings[-1]
        return [i for i, row in enumerate(self.table) if not row[root_str]]

    def get_truth_values(self) -> List[bool]:
        root_str = self.node_strings[-1]
        return [row[root_str] for row in self.table]

    def get_index_form(self) -> str:
        truth_values = self.get_truth_values()
        binary_str = "".join("1" if val else "0" for val in truth_values)
        decimal = int(binary_str, 2)
        return f"{decimal} - {binary_str}"


# class NodeVisitor:
#     def visit(self, node: ExpressionNode):
#         method_name = 'visit_' + type(node).__name__
#         visitor = getattr(self, method_name, self.generic_visit)
#         return visitor(node)

#     def generic_visit(self, node):
#         raise Exception('No visit_{} method'.format(type(node).__name__))

# class TruthTable(NodeVisitor):
#     def __init__(self, logical_function: LogicalFunction):
#         self.logical_function = logical_function
#         self.variables = self.logical_function.variables
#         self.head = self.variables[:]
#         self.generate_head()
#         self.table = []
#         self.fill_table()

#     def visit_BinaryOperationNode(self, node: BinaryOperationNode):
#         left_value = self.visit(node.left_opd)
#         right_value = self.visit(node.right_opd)
#         result = f"({left_value} {node.opr.value} {right_value})"
#         if result not in self.head:
#             self.head.append(result)
#         return result

#     def visit_UnaryOperationNode(self, node: UnaryOperationNode):
#         value = self.visit(node.opd)
#         result = f"({node.opr.value} {value})"
#         if result not in self.head:
#             self.head.append(result)
#         return result

#     def visit_VariableNode(self, node: VariableNode):
#         return node.name

#     def generate_head(self):
#         return self.visit(self.logical_function.ast)

#     def fill_table(self):
#         num_vars = len(self.variables)
#         possible_value_combinations = itertools.product([False, True], repeat=num_vars)
#         for values in possible_value_combinations:
#             assignment = dict(zip(self.variables, values))
#             result = tuple(map(lambda x: int(x), values)) + (int(self.logical_function.ast.evaluate(assignment)), )
#             self.table.append((result))

#     def print_table(self):
#         print(self.head)
#         for row in self.table:
#             print(*row, sep=" | ")
