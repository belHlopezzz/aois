from typing import List, Dict
from itertools import product
from tabulate import tabulate

from logic.table_truth.logical_function import LogicalFunction


class TruthTable:
    def __init__(
        self,
        *,
        logical_function: LogicalFunction = None,
        table: List[List[int]] = None,
        variables: List[str] = None,
    ):
        self.num_form_pcnf = []
        self.num_form_pdnf = []

        if logical_function is not None:
            self.logical_function = logical_function
            self.variables = logical_function.variables
            self.table = []
            self._generate_table()
        elif table is not None and variables is not None:
            self.logical_function = None
            self.variables = variables
            self.table = table
            self._calculate_forms()

    def _calculate_forms(self) -> None:
        for i, row in enumerate(self.table):
            result = row[-1]
            if result == 1:
                self.num_form_pdnf.append(i)
            else:
                self.num_form_pcnf.append(i)

    def _generate_table(self) -> List[List[int]]:
        combinations = product([0, 1], repeat=len(self.variables))
        for i, combination in enumerate(combinations):
            assignment = dict(zip(self.variables, combination))
            result = int(self.logical_function.evaluate(assignment))

            if result == 1:
                self.num_form_pdnf.append(i)
            else:
                self.num_form_pcnf.append(i)

            row = list(combination) + [result]
            self.table.append(row)

    def display(self) -> str:
        headers = self.variables + ["Result"]
        print(tabulate(self.table, headers=headers, tablefmt="simple_grid"))

    def get_num_form_pdnf(self) -> str:
        str_num_form_pdnf = map(lambda x: str(x), self.num_form_pdnf)
        return f"({", ".join(str_num_form_pdnf)}) |"

    def get_num_form_pcnf(self) -> str:
        str_num_form_pdnf = map(lambda x: str(x), self.num_form_pcnf)
        return f"({", ".join(str_num_form_pdnf)}) &"

    def get_index_form(self) -> str:
        result = ["0"] * 2 ** len(self.variables)
        for i in self.num_form_pdnf:
            result[i] = "1"
        return "".join(result)

    def get_pcnf(self) -> str:
        maxterms = []
        for j in self.num_form_pcnf:
            terms = [
                f"!{var}" if self.table[j][i] else var
                for i, var in enumerate(self.variables)
            ]
            maxterm = "(" + "|".join(terms) + ")"
            maxterms.append(maxterm)
        return "&".join(maxterms)

    def get_pdnf(self) -> str:
        minterms = []
        for j in self.num_form_pdnf:
            terms = [
                var if self.table[j][i] else f"!{var}"
                for i, var in enumerate(self.variables)
            ]
            minterm = "(" + "&".join(terms) + ")"
            minterms.append(minterm)
        return "|".join(minterms)

    def group_pdnf(self) -> Dict[int, List[List[int]]]:
        groups = {}
        for pdnf in self.num_form_pdnf:
            row = self.table[pdnf][:-1]
            groups.setdefault(row.count(1), []).append(row)
        return groups

    def group_pcnf(self) -> Dict[int, List[List[int]]]:
        groups = {}
        for pcnf in self.num_form_pcnf:
            row = self.table[pcnf][:-1]
            groups.setdefault(row.count(1), []).append(row)
        return groups

    def get_pdnf_constituents(self):
        return [self.table[i][:-1] for i in self.num_form_pdnf]

    def get_pcnf_constituents(self):
        return [self.table[i][:-1] for i in self.num_form_pcnf]
