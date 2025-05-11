from typing import Dict, List, Tuple, Optional
from tabulate import tabulate
from itertools import product

from src.pnf_contructor.truth_table import TruthTable


class Minimizer:
    def __init__(self, truth_table: TruthTable) -> None:
        self.truth_table = truth_table
        self.variables = self.truth_table.variables
        self.variables_count = len(self.variables)

    # ------------------------------------------------------------
    # -------------------------- MERGING --------------------------
    # ------------------------------------------------------------
    @staticmethod
    def print_group(group: Dict[int, List[List[bool]]]) -> None:
        for group_num in sorted(group.keys()):
            constituents = group[group_num]
            formatted_constituents = [
                "".join(map(str, constituent)) for constituent in constituents
            ]
            print(f"Group {group_num}: {', '.join(formatted_constituents)}")
        print()

    @staticmethod
    def merge_groups(
        pnf_group: Dict[int, List[List[int]]], display_merging: bool = True
    ) -> List[List]:
        changed = True
        if display_merging:
            Minimizer.print_group(pnf_group)
        while changed:
            changed = False
            result_groups = {}
            used_constituents = set()

            for group_num in sorted(pnf_group):
                if group_num + 1 in pnf_group:
                    for first_constituent in pnf_group[group_num]:
                        for second_constituent in pnf_group[group_num + 1]:
                            if Minimizer.can_merge(
                                first_constituent, second_constituent
                            ):
                                diff_index = Minimizer.is_one_bit_different(
                                    first_constituent, second_constituent
                                )
                                merged_constituent = Minimizer.merge(
                                    first_constituent, second_constituent, diff_index
                                )
                                key = group_num
                                if merged_constituent not in result_groups.get(key, []):
                                    result_groups.setdefault(key, []).append(
                                        merged_constituent
                                    )
                                used_constituents.add(tuple(first_constituent))
                                used_constituents.add(tuple(second_constituent))
                                changed = True

            if changed and display_merging:
                Minimizer.print_group(result_groups)
            for group_num in pnf_group:
                for constituent in pnf_group[group_num]:
                    if tuple(constituent) not in used_constituents:
                        result_groups.setdefault(group_num, []).append(
                            list(constituent)
                        )

            pnf_group = result_groups

        return [imp for group in pnf_group.values() for imp in group]

    @staticmethod
    def can_merge(
        first_constituent: List[bool], second_constituent: List[bool]
    ) -> bool:
        diff_index = Minimizer.is_one_bit_different(
            first_constituent, second_constituent
        )
        if diff_index == -1:
            return False
        if "*" in first_constituent or "*" in second_constituent:
            return Minimizer.asterisks_position_check(
                first_constituent, second_constituent
            )
        return True

    @staticmethod
    def merge(
        first_constituent: List[bool], second_constituent: List[bool], diff_index: int
    ) -> List:
        return (
            first_constituent[:diff_index] + ["*"] + first_constituent[diff_index + 1 :]
        )

    @staticmethod
    def is_one_bit_different(
        first_constituent: List[bool], second_constituent: List[bool]
    ) -> int:
        index_of_difference = -1
        for i in range(len(first_constituent)):
            if first_constituent[i] != second_constituent[i]:
                if index_of_difference != -1:
                    return -1
                index_of_difference = i
        return index_of_difference

    @staticmethod
    def asterisks_position_check(
        first_constituent: List[bool], second_constituent: List[bool]
    ) -> bool:
        return all(
            (x == "*") == (y == "*")
            for x, y in zip(first_constituent, second_constituent)
        )

    # ------------------------------------------------------------
    # -------------------------- MATRIX --------------------------
    # ------------------------------------------------------------
    @staticmethod
    def create_implicant_matrix(
        implicants: List[List], constituents: List[List]
    ) -> List[List]:
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
    def correspon_to_bin(constituent: List, implicant: List) -> bool:
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
    def found_unique_implicant(implicant_matrix: List[List]) -> Tuple[int, ...]:
        unique_implicant_indexes = set()

        for j in range(1, len(implicant_matrix[0])):
            index = -1

            for i in range(len(implicant_matrix)):
                if implicant_matrix[i][j] == "X":
                    if index != -1:
                        break
                    index = i
            else:
                unique_implicant_indexes.add(index)

        return tuple(unique_implicant_indexes)

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

    def computational_table_minimization(
        self, *, is_pdnf: bool, display_merging: bool = True, display_table: bool = True
    ) -> str:
        result_groups = Minimizer.merge_groups(
            self.truth_table.group_pdnf() if is_pdnf else self.truth_table.group_pcnf(),
            display_merging,
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

        if display_table:
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
    def computational_minimization(
        self, *, is_pdnf: bool, display_merging: bool = True
    ) -> str:
        group = (
            self.truth_table.group_pdnf() if is_pdnf else self.truth_table.group_pcnf()
        )
        implicants = Minimizer.merge_groups(group, display_merging)
        constituents = (
            self.truth_table.get_pdnf_constituents()
            if is_pdnf
            else self.truth_table.get_pcnf_constituents()
        )

        changed = True
        while changed:
            changed = False
            for current_implicant in implicants[:]:
                covered_constituents = [
                    c
                    for c in constituents
                    if Minimizer.correspon_to_bin(c, current_implicant)
                ]
                if not covered_constituents:
                    continue

                is_redundant = all(
                    any(
                        Minimizer.correspon_to_bin(c, other_implicant)
                        for other_implicant in implicants
                        if other_implicant != current_implicant
                    )
                    for c in covered_constituents
                )
                if is_redundant:
                    implicants.remove(current_implicant)
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

    @staticmethod
    def to_binary(number: int, width: int) -> str:
        return format(number, "0" + str(width) + "b")

    def generate_karnaugh_map(
        self,
    ) -> Tuple[List[List[int]], List[str], List[str], List[int], List[int], int, int]:
        if self.variables_count > 5:
            raise ValueError("Karnaugh map for more than 5 variables is not supported.")

        row_var_num = self.variables_count // 2
        col_var_num = self.variables_count - row_var_num
        row_size = 2**row_var_num
        col_size = 2**col_var_num

        row_seq = sorted(range(row_size), key=lambda x: x ^ (x >> 1))
        col_seq = sorted(range(col_size), key=lambda x: x ^ (x >> 1))

        karnaugh_map = [[0 for _ in range(col_size)] for _ in range(row_size)]
        for i in range(row_size):
            for j in range(col_size):
                index = (row_seq[i] << col_var_num) | col_seq[j]
                karnaugh_map[i][j] = self.truth_table.table[index][-1]

        row_labels = [
            Minimizer.to_binary(k ^ (k >> 1), row_var_num) for k in range(row_size)
        ]
        col_labels = [
            Minimizer.to_binary(k ^ (k >> 1), col_var_num) for k in range(col_size)
        ]
        return (
            karnaugh_map,
            row_labels,
            col_labels,
            row_seq,
            col_seq,
            row_var_num,
            col_var_num,
        )

    def display_karnaugh_map(
        self,
        karnaugh_map: List[List[int]],
        row_labels: List[str],
        col_labels: List[str],
        row_var_num: int,
    ) -> None:
        table = []
        for i, row_label in enumerate(row_labels):
            row = [row_label] + [karnaugh_map[i][j] for j in range(len(col_labels))]
            table.append(row)
        var_tag = (
            "".join(self.variables[:row_var_num])
            + "\\"
            + "".join(self.variables[row_var_num:])
        )
        headers = [var_tag] + col_labels
        print(tabulate(table, headers=headers, tablefmt="simple_grid"))

    def karnaugh_map_minimization(
        self, *, is_pdnf: bool, display_karnaugh_map: bool = True
    ) -> str:
        (
            karnaugh_map,
            row_labels,
            col_labels,
            row_seq,
            col_seq,
            row_var_num,
            col_var_num,
        ) = self.generate_karnaugh_map()

        if display_karnaugh_map:
            self.display_karnaugh_map(karnaugh_map, row_labels, col_labels, row_var_num)

        # Determine target value (1 for PDNF, 0 for PCNF)
        target_value = 1 if is_pdnf else 0
        positions_to_cover = [
            (i, j)
            for i in range(2**row_var_num)
            for j in range(2**col_var_num)
            if karnaugh_map[i][j] == target_value
        ]
        if not positions_to_cover:
            return "Doesn't exist"

        # Build all valid grouping assignments
        possible_assignments = product([None, 0, 1], repeat=self.variables_count)
        groups: List[Tuple[Tuple[Optional[int], ...], List[Tuple[int, int]]]] = []
        for assignment in possible_assignments:
            group = self.get_group(
                assignment, row_seq, col_seq, row_var_num, col_var_num
            )
            if group and all(karnaugh_map[i][j] == target_value for i, j in group):
                groups.append((assignment, group))

        # Greedy select groups to cover all target positions
        selected_groups: List[Tuple[Tuple[Optional[int], ...], List[Tuple[int, int]]]] = []
        covered: set = set()
        while covered != set(positions_to_cover):
            best_group = max(
                groups,
                key=lambda grp: len(set(grp[1]) - covered),
                default=None,
            )
            if not best_group or len(set(best_group[1]) - covered) == 0:
                raise ValueError("Cannot cover all positions with Karnaugh grouping")
            selected_groups.append(best_group)
            covered |= set(best_group[1])

        # Remove redundant groups: if removing a group still covers all, drop it
        final_groups = selected_groups.copy()
        for grp in selected_groups:
            others = [g for g in final_groups if g != grp]
            # Compute coverage without this group
            cover_without = set()
            for _, cells in others:
                cover_without |= set(cells)
            if set(positions_to_cover).issubset(cover_without):
                final_groups.remove(grp)
        selected_groups = final_groups

        # Convert to variable terms
        terms = [
            self.group_to_term(assignment, is_pdnf)
            for assignment, _ in selected_groups
        ]
        if is_pdnf:
            minimized_form = "(" + ")|(".join(terms) + ")"
        else:
            minimized_form = "(" + ")&(".join(terms) + ")"
        return minimized_form

    def get_group(
        self,
        assignment: Tuple[Optional[int], ...],
        row_seq: List[int],
        col_seq: List[int],
        row_var_num: int,
        col_var_num: int,
    ) -> Optional[List[Tuple[int, int]]]:
        n = len(assignment)
        group = []
        for i in range(2**row_var_num):
            for j in range(2**col_var_num):
                index = (row_seq[i] << col_var_num) | col_seq[j]
                binary = Minimizer.to_binary(index, n)
                satisfies = all(
                    assignment[k] is None or int(binary[k]) == assignment[k]
                    for k in range(n)
                )
                if satisfies:
                    group.append((i, j))
        return group

    def select_minimal_cover(
        self,
        groups: List[Tuple[Tuple[Optional[int], ...], List[Tuple[int, int]]]],
        positions_to_cover: List[Tuple[int, int]],
    ) -> List[Tuple[Tuple[Optional[int], ...], List[Tuple[int, int]]]]:
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

    def group_to_term(
        self, assignment: Tuple[Optional[int], ...], is_pdnf: bool
    ) -> str:
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

        if not terms:
            return "1" if is_pdnf else "0"

        return "&".join(terms) if is_pdnf else "|".join(terms)
