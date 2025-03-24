import sys

sys.path.insert(
    0, "C:\\Education\\University\\АОИС\\lab_1\\src\\digit_representation\\"
)

from binary_data_types import BinaryInt
import pytest


@pytest.mark.parametrize(
    "decimal_num, binary_num", [(7, "111"), (1, "1"), (10, "1010"), (255, "11111111")]
)
def test_number_conversion_not_signed(decimal_num: int, binary_num: str):
    assert BinaryInt._get_binary_simple(decimal_num) == binary_num


@pytest.mark.parametrize(
    "first_num, second_num, bits_num, result",
    [("10000", "10000", 5, "100000"), ("01100010", "00001000", 8, "01101010")],
)
def test_binary_sum_default(
    first_num: str, second_num: str, bits_num: int, result: str
):
    assert BinaryInt._binary_sum(first_num, second_num, bits_number=bits_num) == result


@pytest.mark.parametrize("decimal_num, bits_num", [(128, 8), (2, 1), (10, 2)])
def test_init_fail(decimal_num: int, bits_num: int):
    with pytest.raises(AssertionError):
        rand_binary = BinaryInt(decimal_num, bits_number=bits_num)


@pytest.mark.parametrize(
    "decimal_num, bits_num, sing, ones, twos",
    [
        (128, 9, "010000000", "010000000", "010000000"),
        (-1024, 12, "110000000000", "101111111111", "110000000000"),
        (0, 1, "0", "0", "0"),
    ],
)
def test_init_success(decimal_num: int, bits_num: int, sing: str, ones: str, twos: str):
    rand_binary = BinaryInt(decimal_num, bits_number=bits_num)
    rand_binary.bits_number = bits_num
    rand_binary.decimal = decimal_num
    rand_binary.sign_magnitude = sing
    rand_binary.ones_complement = ones
    rand_binary.twos_complement = twos


def test_get_binary():
    rand_binary = BinaryInt(11)
    assert "0001011" == rand_binary._get_binary()


@pytest.mark.parametrize(
    "dec_num, result", [(11, "00001011"), (120, "01111000"), (-124, "11111100")]
)
def test_get_sing_magnitude(dec_num: int, result: str):
    assert result == BinaryInt(dec_num)._get_sign_magnitude()


@pytest.mark.parametrize(
    "dec_num, result", [(11, "00001011"), (120, "01111000"), (-124, "10000011")]
)
def test_get_ones_complement(dec_num: int, result: str):
    assert result == BinaryInt(dec_num)._get_ones_complement()


@pytest.mark.parametrize(
    "dec_num, result", [(11, "00001011"), (120, "01111000"), (-124, "10000100")]
)
def test_get_twos_complement(dec_num: int, result: str):
    assert result == BinaryInt(dec_num)._get_twos_complement()


@pytest.mark.parametrize(
    "dec_num1, dec_num2, result", [(11, 12, 23), (0, -56, -56), (-124, 127, 3)]
)
def test_addition_success(dec_num1: int, dec_num2: int, result: int):
    assert (BinaryInt(dec_num1) + BinaryInt(dec_num2)).decimal == result


@pytest.mark.parametrize("dec_num1, dec_num2", [(124, 12), (-125, -56)])
def test_addition_fail(dec_num1: int, dec_num2: int):
    with pytest.raises(OverflowError):
        BinaryInt(dec_num1) + BinaryInt(dec_num2)


@pytest.mark.parametrize(
    "dec_num1, dec_num2, result", [(11, 12, -1), (0, -56, 56), (124, 127, -3)]
)
def test_substraction(dec_num1: int, dec_num2: int, result: int):
    assert (BinaryInt(dec_num1) - BinaryInt(dec_num2)).decimal == result


@pytest.mark.parametrize(
    "dec_num1, dec_num2, result", [(11, 11, 121), (0, -56, 0), (124, 127, 15748)]
)
def test_multiplication(dec_num1: int, dec_num2: int, result: int):
    assert (BinaryInt(dec_num1) * BinaryInt(dec_num2)).decimal == result


@pytest.mark.parametrize(
    "dec_num1, dec_num2, result",
    [
        (11, 12, "0.11101"),
        (0, -56, "0.0"),
        (124, 4, "011111."),
        (12, -4, "111."),
    ],
)
def test_division_success(dec_num1: int, dec_num2: int, result: str):
    assert (BinaryInt(dec_num1) / BinaryInt(dec_num2)).binary_float == result


@pytest.mark.parametrize("dec_num1, dec_num2", [(41, 0), (0, 0)])
def test_division_fail(dec_num1: int, dec_num2: int):
    with pytest.raises(ZeroDivisionError):
        BinaryInt(dec_num1) / BinaryInt(dec_num2)


def test_int_represenation():
    rand_binary = BinaryInt(-4)
    assert rand_binary.__str__() == (
        f"\nDecimal representation: {-4}\n"
        f"Binary representation:\n"
        f"  - Sign magnitude: {"10000100"}\n"
        f"  - One's complement: {"11111011"}\n"
        f"  - Two's complement: {"11111100"}\n"
    )
