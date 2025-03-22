class BinaryFloatFixed:
    ACCURACY = 5

    def __init__(self, decimal_float: float, precision: int = ACCURACY):
        self.decimal_float = decimal_float
        self.binary_float = self._get_binary_fixed()

    def _get_binary_fixed(self):
        sign = "1" if self.decimal_float >= 0 else "0"
        decimal_float_abs = abs(self.decimal_float)
        int_part = int(decimal_float_abs)
        float_part = decimal_float_abs - int_part
        print(float_part)
        int_part_str = int_binaries.BinaryInt._get_binary(int_part)

    def __str__(self):
        return (
            f"\nDecimal representation: {self.decimal_float}\n"
            f"Binary representation: {self.binary_float}\n"
        )


class BinaryFloatIEEE:
    EXPONENTA_LENGTH = 8
    MANTISSA_LENGTH = 23

    def __init__():
        pass
