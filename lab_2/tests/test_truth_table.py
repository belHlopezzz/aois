import pytest
from table_truth_generator.logical_function import LogicalFunction
from table_truth_generator.truth_table import TruthTable


def test_truth_table_initialization():
    func = LogicalFunction("x & y")
    table = TruthTable(func)
    assert table.logical_function == func
    assert table.variables == ["x", "y"]
    assert len(table.table) == 4
    assert len(table.table[0]) == 3


def test_truth_table_generation():
    func = LogicalFunction("x & y")
    table = TruthTable(func)

    expected_table = [
        [False, False, False],
        [False, True, False],
        [True, False, False],
        [True, True, True],
    ]
    assert table.table == expected_table


def test_truth_table_display(capsys):
    func = LogicalFunction("x & y")
    table = TruthTable(func)
    table.display()
    captured = capsys.readouterr()
    assert "x" in captured.out
    assert "y" in captured.out
    assert "x & y" in captured.out


def test_truth_table_num_forms():
    func = LogicalFunction("x & y")
    table = TruthTable(func)

    assert table.num_form_pdnf == [3]
    assert table.num_form_pcnf == [0, 1, 2]

    assert table.get_num_form_pdnf() == "(3) |"
    assert table.get_num_form_pcnf() == "(0, 1, 2) &"


def test_truth_table_index_form():
    func = LogicalFunction("x & y")
    table = TruthTable(func)
    assert table.get_index_form() == "0001"


def test_truth_table_pcnf():
    func = LogicalFunction("x & y")
    table = TruthTable(func)
    expected_pcnf = "(x|y)&(x|!y)&(!x|y)"
    assert table.get_pcnf() == expected_pcnf


def test_truth_table_pdnf():
    func = LogicalFunction("x & y")
    table = TruthTable(func)
    expected_pdnf = "(x&y)"
    assert table.get_pdnf() == expected_pdnf


def test_truth_table_complex_expression():
    func = LogicalFunction("!(x & y) | z")
    table = TruthTable(func)

    assert len(table.table) == 8
    assert len(table.table[0]) == 4

    expected_table = [
        [False, False, False, True],
        [False, False, True, True],
        [False, True, False, True],
        [False, True, True, True],
        [True, False, False, True],
        [True, False, True, True],
        [True, True, False, False],
        [True, True, True, True],
    ]
    assert table.table == expected_table

    assert table.get_index_form() == "11111101"
    assert table.num_form_pdnf == [0, 1, 2, 3, 4, 5, 7]
    assert table.num_form_pcnf == [6]


def test_truth_table_equivalence():
    func = LogicalFunction("x ~ y")
    table = TruthTable(func)

    expected_table = [
        [False, False, True],
        [False, True, False],
        [True, False, False],
        [True, True, True],
    ]
    assert table.table == expected_table

    assert table.get_index_form() == "1001"
    assert table.num_form_pdnf == [0, 3]
    assert table.num_form_pcnf == [1, 2]


def test_truth_table_implication():
    func = LogicalFunction("x > y")
    table = TruthTable(func)

    expected_table = [
        [False, False, True],
        [False, True, True],
        [True, False, False],
        [True, True, True],
    ]
    assert table.table == expected_table

    assert table.get_index_form() == "1101"
    assert table.num_form_pdnf == [0, 1, 3]
    assert table.num_form_pcnf == [2]
