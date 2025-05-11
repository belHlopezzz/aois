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


def test_computational_table_minimization_simple_dnf(minimizer_simple):
    result = minimizer_simple.computational_table_minimization(
        is_pdnf=True, display_merging=False, display_table=False
    )
    assert result == "(a&b)"


def test_computational_table_minimization_simple_cnf(minimizer_simple):
    result = minimizer_simple.computational_table_minimization(
        is_pdnf=False, display_merging=False, display_table=False
    )
    assert result == "(a)&(b)"


def test_computational_table_minimization_complex_dnf(minimizer_complex):
    result = minimizer_complex.computational_table_minimization(
        is_pdnf=True, display_merging=False, display_table=False
    )
    assert result == "(!a&c)|(a&b)"


def test_computational_table_minimization_complex_cnf(minimizer_complex):
    result = minimizer_complex.computational_table_minimization(
        is_pdnf=False, display_merging=False, display_table=False
    )
    assert result == "(a|c)&(!a|b)"


def test_create_implicant_matrix():
    implicants = [[1, 0, "*"], [1, "*", 1]]
    constituents = [[1, 0, 0], [1, 0, 1], [1, 1, 1]]
    matrix = Minimizer.create_implicant_matrix(implicants, constituents)
    assert len(matrix) == 2
    assert len(matrix[0]) == 4  # row_name + 3 constituents
    assert matrix[0][0] == "10*"
    assert matrix[1][0] == "1*1"


def test_correspon_to_bin():
    assert Minimizer.correspon_to_bin([1, 0, 1], [1, "*", 1])
    assert not Minimizer.correspon_to_bin([1, 0, 1], [1, "*", 0])
    assert Minimizer.correspon_to_bin([1, 0, 1], [1, 0, "*"])


def test_found_unique_implicant():
    matrix = [["10*", "X", "X", " "], ["1*1", " ", "X", "X"], ["*11", " ", " ", "X"]]
    unique = Minimizer.found_unique_implicant(matrix)
    assert len(unique) > 0
    assert isinstance(unique, tuple)


def test_convert_bin_to_var_form(minimizer_simple):
    implicant = [1, 0, "*"]
    dnf_result = minimizer_simple.convert_bin_to_var_form(implicant, is_pdnf=True)
    cnf_result = minimizer_simple.convert_bin_to_var_form(implicant, is_pdnf=False)
    assert dnf_result == "a&!b"
    assert cnf_result == "!a|b"
