from typing import List, Tuple
from itertools import product
from tabulate import tabulate

from logical_function import LogicalFunction


class TruthTable:
    def __init__(self, logical_function: LogicalFunction):
        self.logical_function = logical_function
        self.variables = logical_function.variables

        self.num_form_pcnf = []
        self.num_form_pdnf = []

        self.table = []
        self._generate_table()


    def _generate_table(self) -> List[List[bool]]:
        combinations = product([False, True], repeat=len(self.variables))
        for i, combination in enumerate(combinations):
            assignment = dict(zip(self.variables, combination))
            result = self.logical_function.evaluate(assignment)

            if result:
                self.num_form_pdnf.append(i)
            else:
                self.num_form_pcnf.append(i)

            row = list(combination) + [result]
            self.table.append(row)

    def display(self) -> str:
        headers = self.variables + [self.logical_function.formula]
        table_data = [[int(cell) for cell in row] for row in self.table]
        print(tabulate(table_data, headers=headers, tablefmt="simple_grid"))

    def get_num_form_pdnf(self) -> str:
        str_num_form_pdnf = map(lambda x: str(x), self.num_form_pdnf)
        return f"({", ".join(str_num_form_pdnf)}) |"
    
    def get_num_form_pcnf(self) -> str:
        str_num_form_pdnf = map(lambda x: str(x), self.num_form_pcnf)
        return f"({", ".join(str_num_form_pdnf)}) &"
    
    def get_index_form(self) -> tuple:
         result = ["0"] * 2 ** len(self.variables)
         for i in self.num_form_pdnf:
              result[i] = "1"
         return "".join(result)

    def get_pcnf(self) -> str:
        result = ""
        for j in self.num_form_pcnf:
                terms = []
                for i in range(len(self.variables)):
                    var = self.variables[i]
                    terms.append(f"{var}" if not self.table[j][i] else f"!{var}")
                result += "(" + "|".join(terms) + ")&"
        return result.rstrip("&") 

    def get_pdnf(self) -> str:
        result = ""
        for j in self.num_form_pdnf:
                terms = []
                for i in range(len(self.variables)):
                    var = self.variables[i]
                    terms.append(f"{var}" if self.table[j][i] else f"!{var}")
                result += "(" + "&".join(terms) + ")|"
        return result.rstrip("|") 
