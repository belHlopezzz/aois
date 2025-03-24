import sys

sys.path.insert(
    0, "C:\\Education\\University\\АОИС\\lab_1\\src\\digit_representation\\"
)

from binary_data_types import BinaryFloatFixed, BinaryFloatIEEE
import pytest


@pytest.mark.parametrize(
    "decimal_num, expected_result",
    [(7.25, "0111.01"), (-128.756, "110000000.11"), (0, "0.0")],
)
def test_default_fixed_float_init(decimal_num: float, expected_result: str):
    rand_binary = BinaryFloatFixed(decimal_num)
    assert rand_binary.binary_float == expected_result


def test_fixed_float_represenation():
    rand_binary = BinaryFloatFixed(-4.25)
    assert rand_binary.__str__() == (
        f"\nDecimal representation (before converting): {"-4.25"}\n"
        f"Decimal representation (after converting): {"-4.25"}\n"
        f"Binary representation (with fixed point): {"1100.01"}\n"
    )


@pytest.mark.parametrize(
    "decimal_num, sign, exponenta, mantissa",
    [
        (78.125, "0", "10000101", "00111000100000000000000"),
        (-1246.87, "1", "10001001", "00110111101101111010111"),
        (0, "0", "00000000", "00000000000000000000000"),
    ],
)
def test_ieee_init_from_fixed_float(
    decimal_num: float, sign: str, exponenta: str, mantissa: str
):
    rand_binary = BinaryFloatFixed(decimal_num, precision=25)
    binary_ieee = BinaryFloatIEEE(rand_binary)
    assert (sign, exponenta, mantissa) == (
        binary_ieee.sign,
        binary_ieee.exponenta,
        binary_ieee.mantissa,
    )


@pytest.mark.parametrize(
    "sign, exponenta, mantissa",
    [
        ("0", "10000101", "00111000100000000000000"),
        ("1", "10001001", "00110111101101111010111"),
        ("0", "00000000", "00000000000000000000000"),
    ],
)
def test_ieee_init_from_sem(sign: str, exponenta: str, mantissa: str):
    binary_ieee = BinaryFloatIEEE(sign=sign, exponenta=exponenta, mantissa=mantissa)
    assert (sign, exponenta, mantissa) == (
        binary_ieee.sign,
        binary_ieee.exponenta,
        binary_ieee.mantissa,
    )
