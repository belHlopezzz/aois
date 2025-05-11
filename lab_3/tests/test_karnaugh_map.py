import pytest
from pnf_contructor.truth_table import TruthTable
from pnf_contructor.logical_function import LogicalFunction
from corno.minimizer import Minimizer


@pytest.fixture
def simple_function():
    return LogicalFunction("a & b")


@pytest.fixture
def complex_function():
    return LogicalFunction("(a & b) | (!a & c)")


@pytest.fixture
def minimizer_simple(simple_function):
    return Minimizer(TruthTable(simple_function))


@pytest.fixture
def minimizer_complex(complex_function):
    return Minimizer(TruthTable(complex_function))


def test_karnaugh_map_minimization_simple_dnf(minimizer_simple):
    result = minimizer_simple.karnaugh_map_minimization(
        is_pdnf=True, display_karnaugh_map=False
    )
    assert result == "(a&b)"


def test_karnaugh_map_minimization_simple_cnf(minimizer_simple):
    result = minimizer_simple.karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=False
    )
    assert result == "(b)&(a)"


def test_karnaugh_map_minimization_complex_dnf(minimizer_complex):
    result = minimizer_complex.karnaugh_map_minimization(
        is_pdnf=True, display_karnaugh_map=False
    )
    assert result == "(!a&c)|(a&b)"


def test_karnaugh_map_minimization_complex_cnf(minimizer_complex):
    result = minimizer_complex.karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=False
    )
    assert result == "(a|c)&(!a|b)"


def test_to_binary():
    assert Minimizer.to_binary(5, 3) == "101"
    assert Minimizer.to_binary(0, 2) == "00"
    assert Minimizer.to_binary(7, 3) == "111"


def test_generate_karnaugh_map(minimizer_simple):
    karnaugh_map, row_labels, col_labels, row_seq, col_seq, row_var_num, col_var_num = (
        minimizer_simple.generate_karnaugh_map()
    )
    assert len(karnaugh_map) == 2
    assert len(karnaugh_map[0]) == 2
    assert len(row_labels) == 2
    assert len(col_labels) == 2
    assert row_var_num == 1
    assert col_var_num == 1


def test_get_group(minimizer_simple):
    assignment = (1, None)
    row_seq = [0, 1]
    col_seq = [0, 1]
    group = minimizer_simple.get_group(assignment, row_seq, col_seq, 1, 1)
    assert group is not None
    assert len(group) > 0
    assert all(isinstance(pos, tuple) for pos in group)


def test_select_minimal_cover(minimizer_simple):
    groups = [((1, None), [(0, 0), (0, 1)]), ((None, 1), [(0, 1), (1, 1)])]
    positions = [(0, 0), (0, 1), (1, 1)]
    selected = minimizer_simple.select_minimal_cover(groups, positions)
    assert len(selected) > 0
    assert all(isinstance(group, tuple) for group in selected)


def test_group_to_term(minimizer_simple):
    assignment = (1, 0, None)
    dnf_result = minimizer_simple.group_to_term(assignment, is_pdnf=True)
    cnf_result = minimizer_simple.group_to_term(assignment, is_pdnf=False)
    assert dnf_result == "a&!b"
    assert cnf_result == "!a|b"


def test_too_many_variables():
    function = LogicalFunction("a & b & c & d & e & f")
    with pytest.raises(ValueError):
        Minimizer(TruthTable(function)).generate_karnaugh_map()
