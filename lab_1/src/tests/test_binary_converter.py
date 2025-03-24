import sys

sys.path.insert(
    0, "C:\\Education\\University\\АОИС\\lab_1\\src\\digit_representation\\"
)

from binary_data_types import BinaryConverter
import pytest


@pytest.mark.parametrize(
    "binary, result",
    [("100010", 34), ("100000000", 256), ("0", 0)],
)
def test_simple_binary_convertion(binary: str, result: int):
    assert result == BinaryConverter.to_decimal(binary)


@pytest.mark.parametrize(
    "binary, result",
    [("01001110", 78), ("1100000010", -258)],
)
def test_sign_magnitude_converter(binary: str, result: int):
    assert result == BinaryConverter.convert_sign_magnitude(binary)


@pytest.mark.parametrize(
    "binary, result",
    [("01001110", 78), ("1011111101", -258)],
)
def test_ones_complete_converter(binary: str, result: int):
    assert result == BinaryConverter.convert_ones_complement(binary)


@pytest.mark.parametrize(
    "binary, result",
    [("01001110", 78), ("1011111110", -258)],
)
def test_twos_complete_converter(binary: str, result: int):
    assert result == BinaryConverter.convert_twos_complement(binary)


@pytest.mark.parametrize(
    "binary, result",
    [("1111.01", -7.25), ("010110111101.001", 1469.125)],
)
def test_fixed_point_converter(binary: str, result: int):
    assert result == BinaryConverter.conver_with_fixed_point(binary)


@pytest.mark.parametrize(
    "sing, exponenta, mantissa, result",
    [
        ("0", "10000101", "00111000100000000000000", 78.125),
        ("1", "10000011", "10011110000000000000000", -25.875),
    ],
)
def test_ieee_converter(sing: str, exponenta: str, mantissa: str, result: int):
    assert result == BinaryConverter.convert_ieee(
        sign=sing, exponenta=exponenta, mantissa=mantissa
    )
