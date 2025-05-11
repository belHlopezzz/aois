from typing import Dict, List
from tabulate import tabulate
from itertools import product, combinations

from pnf_contructor.truth_table import TruthTable


class Minimizer:
    def __init__(self, truth_table: TruthTable):
        self.truth_table = truth_table
        self.variables = self.truth_table.variables

    # ------------------------------------------------------------
    # -------------------------- MERGING --------------------------
    # ------------------------------------------------------------
    @staticmethod
    def print_group(group: Dict[int, List[List[bool]]]):
        for group_num in sorted(group.keys()):
            constituents = group[group_num]
            formatted_constituents = [
                "".join(map(str, constituent)) for constituent in constituents
            ]
            print(f"Group {group_num}: {', '.join(formatted_constituents)}")
        print()

    @staticmethod
    def merge_groups(pnf_group: Dict[int, List[List[int]]]) -> List[List]:
        changed = True
        Minimizer.print_group(pnf_group)
        while changed:
            changed = False
            result_groups = {}
            used = set()

            for group_num in sorted(pnf_group):
                if group_num + 1 in pnf_group:
                    for elem1 in pnf_group[group_num]:
                        for elem2 in pnf_group[group_num + 1]:
                            if Minimizer.can_merge(elem1, elem2):
                                diff_index = Minimizer.is_one_bit_different(
                                    elem1, elem2
                                )
                                new_elem = Minimizer.merge(elem1, elem2, diff_index)
                                key = group_num
                                if new_elem not in result_groups.get(key, []):
                                    result_groups.setdefault(key, []).append(new_elem)
                                used.add(tuple(elem1))
                                used.add(tuple(elem2))
                                changed = True

            if changed:
                Minimizer.print_group(result_groups)
            for group_num in pnf_group:
                for elem in pnf_group[group_num]:
                    if tuple(elem) not in used:
                        result_groups.setdefault(group_num, []).append(list(elem))

            pnf_group = result_groups

        return [imp for group in pnf_group.values() for imp in group]

    @staticmethod
    def can_merge(constituent1, constituent2) -> bool:
        diff_index = Minimizer.is_one_bit_different(constituent1, constituent2)
        if diff_index == -1:
            return False
        if "*" in constituent1 or "*" in constituent2:
            return Minimizer.asterisks_position_check(constituent1, constituent2)
        return True

    @staticmethod
    def merge(constituent1, constituent2, diff_index) -> List:
        return constituent1[:diff_index] + ["*"] + constituent1[diff_index + 1 :]

    @staticmethod
    def is_one_bit_different(
        constituent_1: List[bool], constituent_2: List[bool]
    ) -> int:
        index_of_difference = -1
        for i in range(len(constituent_1)):
            if constituent_1[i] != constituent_2[i]:
                if index_of_difference != -1:
                    return -1
                index_of_difference = i
        return index_of_difference

    @staticmethod
    def asterisks_position_check(
        constituent_1: List[bool], constituent_2: List[bool]
    ) -> bool:
        return all(
            (x == "*") == (y == "*") for x, y in zip(constituent_1, constituent_2)
        )

    # ------------------------------------------------------------
    # -------------------------- MATRIX --------------------------
    # ------------------------------------------------------------
    @staticmethod
    def create_implicant_matrix(implicants, constituents):
        result = []
        for implicant in implicants:
            row_name = "".join(str(el) if el != "*" else "*" for el in implicant)
            row = [row_name]
            for constituent in constituents:
                if Minimizer.correspon_to_bin(constituent, implicant):
                    row.append("X")
                else:
                    row.append(" ")
            result.append(row)
        return result

    @staticmethod
    def correspon_to_bin(constituent, implicant: List):
        for el1, el2 in zip(constituent, implicant):
            if el2 == "*":
                continue
            if el1 != el2:
                return False
        return True

    # ------------------------------------------------------------
    # ---------------- COMPUTATIONAL-TABLE-MINIMIZATION ---------
    # ------------------------------------------------------------
    @staticmethod
    def found_unique_implicant(implicant_matrix: List[List]):
        res_implicants_indexes = set()

        for j in range(1, len(implicant_matrix[0])):
            index = -1

            for i in range(len(implicant_matrix)):
                if implicant_matrix[i][j] == "X":
                    if index != -1:
                        break
                    index = i
            else:
                res_implicants_indexes.add(index)

        return tuple(res_implicants_indexes)

    def convert_bin_to_var_form(self, implicant: List, is_pdnf: bool) -> str:
        if is_pdnf:
            result = [
                f"{"!" if not var else ""}{self.truth_table.variables[i]}"
                for i, var in enumerate(implicant)
                if var != "*"
            ]
            return "&".join(result)
        else:
            result = [
                f"{"!" if var else ""}{self.truth_table.variables[i]}"
                for i, var in enumerate(implicant)
                if var != "*"
            ]
            return "|".join(result)

    def computational_table_minimization(self, *, is_pdnf: bool):
        result_groups = Minimizer.merge_groups(
            self.truth_table.group_pdnf() if is_pdnf else self.truth_table.group_pcnf()
        )
        constituents = (
            self.truth_table.get_pdnf_constituents()
            if is_pdnf
            else self.truth_table.get_pcnf_constituents()
        )

        implicant_matrix = Minimizer.create_implicant_matrix(
            result_groups, constituents
        )
        unique_implicants = Minimizer.found_unique_implicant(implicant_matrix)

        if is_pdnf:
            result = [
                f"({self.convert_bin_to_var_form(result_groups[i], is_pdnf)})"
                for i in unique_implicants
            ]
            result = "|".join(result)
        else:
            result = [
                f"({self.convert_bin_to_var_form(result_groups[i], is_pdnf)})"
                for i in unique_implicants
            ]
            result = "&".join(result)

        column_headers = [""] + ["".join(map(str, comb)) for comb in constituents]
        print(
            tabulate(
                implicant_matrix,
                headers=column_headers,
                tablefmt="simple_grid",
                stralign="center",
            )
        )

        return result

    # ------------------------------------------------------------
    # ---------------- COMPUTATIONAL-MINIMIZATION ---------------
    # ------------------------------------------------------------
    @staticmethod
    def remove_redundant_implicants(implicants: List[List[bool]]):
        i = 0
        while i < len(implicants):
            implicant1 = implicants[i]
            j = 0
            while j < len(implicants):
                if i == j:
                    j += 1
                    continue
                implicant2 = implicants[j]
                if all(
                    k == z
                    for k, z in zip(implicant1, implicant2)
                    if k != "*" and z != "*"
                ):
                    implicants.pop(j)
                    break
                j += 1
            i += 1

        return implicants

    def computational_minimization(self, *, is_pdnf: bool):
        group = (
            self.truth_table.group_pdnf() if is_pdnf else self.truth_table.group_pcnf()
        )
        implicants = Minimizer.merge_groups(group)
        constituents = (
            self.truth_table.get_pdnf_constituents()
            if is_pdnf
            else self.truth_table.get_pcnf_constituents()
        )

        changed = True
        while changed:
            changed = False
            for imp in implicants[:]:
                const_covered = [
                    c for c in constituents if Minimizer.correspon_to_bin(c, imp)
                ]
                if not const_covered:
                    continue

                is_redundant = all(
                    any(
                        Minimizer.correspon_to_bin(c, other)
                        for other in implicants
                        if other != imp
                    )
                    for c in const_covered
                )
                if is_redundant:
                    implicants.remove(imp)
                    changed = True
                    break

        if is_pdnf:
            result = [
                f"({self.convert_bin_to_var_form(imp, is_pdnf)})" for imp in implicants
            ]
            result = "|".join(result)
        else:
            result = [
                f"({self.convert_bin_to_var_form(imp, is_pdnf)})" for imp in implicants
            ]
            result = "&".join(result)

        return result

    # ------------------------------------------------------------
    # ---------------- KARNAUGH-MAP-MINIMIZATION ----------------
    # ------------------------------------------------------------

    staticmethod
    def to_binary(k, w):
        return format(k, '0' + str(w) + 'b')

    def generate_karnaugh_map(self):
        n = len(self.variables)
        if n > 5:
            raise ValueError("Karnaugh map for more than 5 variables is not supported.")
        r = n // 2
        s = n - r
        row_size = 2 ** r
        col_size = 2 ** s
        # Generate the sequence for rows and columns
        row_seq = sorted(range(row_size), key=lambda x: x ^ (x >> 1))
        col_seq = sorted(range(col_size), key=lambda x: x ^ (x >> 1))
        # Create the map
        karnaugh_map = [[0 for _ in range(col_size)] for _ in range(row_size)]
        for i in range(row_size):
            for j in range(col_size):
                index = (row_seq[i] << s) | col_seq[j]
                karnaugh_map[i][j] = self.truth_table.table[index][-1]
        # Generate labels
        row_labels = [Minimizer.to_binary(k ^ (k >> 1), r) for k in range(row_size)]
        col_labels = [Minimizer.to_binary(k ^ (k >> 1), s) for k in range(col_size)]
        return karnaugh_map, row_labels, col_labels, row_seq, col_seq, r, s

    def display_karnaugh_map(self):
        karnaugh_map, row_labels, col_labels, _, _, _, _ = self.generate_karnaugh_map()
        table = []
        for i, row_label in enumerate(row_labels):
            row = [row_label] + [karnaugh_map[i][j] for j in range(len(col_labels))]
            table.append(row)
        headers = [""] + col_labels
        print(tabulate(table, headers=headers, tablefmt="simple_grid"))

    def karnaugh_map_minimization(self, *, is_pdnf: bool):
        karnaugh_map, row_labels, col_labels, row_seq, col_seq, r, s = self.generate_karnaugh_map()
        self.display_karnaugh_map()
        target_value = 1 if is_pdnf else 0
        positions_to_cover = [(i,j) for i in range(2**r) for j in range(2**s) if karnaugh_map[i][j] == target_value]
        if not positions_to_cover:
            return "0" if is_pdnf else "1"
        # Generate all possible groups
        n = len(self.variables)
        possible_assignments = product([None, 0, 1], repeat=n)
        groups = []
        for assignment in possible_assignments:
            group = self.get_group(assignment, row_seq, col_seq, r, s)
            if group and all(karnaugh_map[i][j] == target_value for i,j in group):
                groups.append((assignment, group))
        # Select a minimal set of groups that cover all positions_to_cover
        selected_groups = self.select_minimal_cover(groups, positions_to_cover)
        # Convert selected groups to terms
        terms = [self.group_to_term(assignment, is_pdnf) for assignment, _ in selected_groups]
        # Combine terms
        if is_pdnf:
            minimized_form = "(" + ')|('.join(terms) + ")"
        else:
            minimized_form = "(" + ')&('.join(terms) + ")"
        return minimized_form

    def get_group(self, assignment, row_seq, col_seq, r, s):
        n = len(assignment)
        group = []
        for i in range(2**r):
            for j in range(2**s):
                index = (row_seq[i] << s) | col_seq[j]
                binary = Minimizer.to_binary(index, n)
                satisfies = all(
                    assignment[k] is None or int(binary[k]) == assignment[k]
                    for k in range(n)
                )
                if satisfies:
                    group.append((i,j))
        return group

    def select_minimal_cover(self, groups, positions_to_cover):
        covered = set()
        selected_groups = []
        while covered != set(positions_to_cover):
            max_cover = 0
            best_group = None
            for group in groups:
                _, g = group
                new_cover = len(set(g) - covered)
                if new_cover > max_cover:
                    max_cover = new_cover
                    best_group = group
            if best_group is None:
                raise ValueError("Cannot cover all positions")
            selected_groups.append(best_group)
            covered |= set(best_group[1])
        return selected_groups

    def group_to_term(self, assignment, is_pdnf):
        n = len(assignment)
        terms = []
        for k in range(n):
            if assignment[k] is not None:
                var = self.variables[k]
                if is_pdnf:
                    term = var if assignment[k] == 1 else f"!{var}"
                else:
                    term = f"!{var}" if assignment[k] == 1 else var
                terms.append(term)
        if is_pdnf:
            return '&'.join(terms) if terms else "1"
        else:
            return '|'.join(terms) if terms else "0"
