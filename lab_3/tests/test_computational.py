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


def test_computational_minimization_simple_dnf(minimizer_simple):
    result = minimizer_simple.computational_minimization(
        is_pdnf=True, display_merging=False
    )
    assert result == "(a&b)"


def test_computational_minimization_simple_cnf(minimizer_simple):
    result = minimizer_simple.computational_minimization(
        is_pdnf=False, display_merging=False
    )
    assert result == "(a)&(b)"


def test_computational_minimization_complex_dnf(minimizer_complex):
    result = minimizer_complex.computational_minimization(
        is_pdnf=True, display_merging=False
    )
    assert result == "(!a&c)|(a&b)"


def test_computational_minimization_complex_cnf(minimizer_complex):
    result = minimizer_complex.computational_minimization(
        is_pdnf=False, display_merging=False
    )
    assert result == "(a|c)&(!a|b)"


def test_merge_groups():
    groups = {1: [[1, 0, 0], [0, 1, 0]], 2: [[1, 1, 0], [0, 1, 1]]}
    result = Minimizer.merge_groups(groups, display_merging=False)
    assert len(result) > 0
    assert any("*" in impl for impl in result)


def test_can_merge():
    assert Minimizer.can_merge([1, 0, 0], [1, 0, 1])
    assert not Minimizer.can_merge([1, 0, 0], [0, 1, 1])
    assert Minimizer.can_merge([1, "*", 0], [1, "*", 1])


def test_is_one_bit_different():
    assert Minimizer.is_one_bit_different([1, 0, 0], [1, 0, 1]) == 2
    assert Minimizer.is_one_bit_different([1, 0, 0], [0, 0, 0]) == 0
    assert Minimizer.is_one_bit_different([1, 0, 0], [1, 1, 0]) == 1
    assert Minimizer.is_one_bit_different([1, 0, 0], [0, 1, 1]) == -1


def test_merge():
    result = Minimizer.merge([1, 0, 0], [1, 0, 1], 2)
    assert result == [1, 0, "*"]


def test_asterisks_position_check():
    assert Minimizer.asterisks_position_check([1, "*", 0], [1, "*", 1])
    assert not Minimizer.asterisks_position_check([1, "*", 0], [1, 0, "*"])
