class BinaryConverter:
    @staticmethod
    def to_decimal(bits: str) -> int:
        return sum(int(bit) * 2**i for i, bit in enumerate(bits[::-1]))

    @staticmethod
    def convert_twos_complement(binary: str) -> int:
        if not all(bit in "01" for bit in binary):
            raise ValueError("Binary string must contain only '0' and '1'")
        result = 0
        for i, bit in enumerate(binary):
            result += (-1 if i == 0 else 1) * int(bit) * 2 ** (len(binary) - 1 - i)
        return result

    @staticmethod
    def convert_ones_complement(binary: str) -> int:
        if not all(bit in "01" for bit in binary):
            raise ValueError("Binary string must contain only '0' and '1'")
        sing = -1 if binary[0] == "1" else 1
        strip_number = (
            "".join("1" if bit == "0" else "0" for bit in binary[1:])
            if sing == -1
            else binary[1:]
        )
        return sing * BinaryConverter.to_decimal(strip_number)

    @staticmethod
    def convert_sign_magnitude(binary: str) -> int:
        if not all(bit in "01" for bit in binary):
            raise ValueError("Binary string must contain only '0' and '1'")
        sing = -1 if binary[0] == "1" else 1
        return sing * BinaryConverter.to_decimal(binary[1:])

    @staticmethod
    def conver_with_fixed_point(binary: str) -> float:
        sign = -1 if binary[0] == "1" else 1
        abs_binary = binary[1:].split(".")
        int_part, float_part = abs_binary[0], abs_binary[1]
        if abs_binary[0]:
            int_part = str(BinaryConverter.to_decimal(int_part))
        else:
            int_part = "0"
        float_part_result = 0
        for i, digit in enumerate(float_part):
            float_part_result += 2 ** (-(i + 1)) * int(digit)
        return (float(int_part) + float_part_result) * sign

    @staticmethod
    def convert_ieee(sign: str, exponenta: str, mantissa: str) -> float:
        if int(sign + exponenta + mantissa) == 0:
            return float(0)
        exponenta_int = BinaryConverter.to_decimal(exponenta) - 127
        result = ""
        if exponenta_int >= 0:
            result = (
                sign + "1" + mantissa[:exponenta_int] + "." + mantissa[exponenta_int:]
            )
        else:
            result = sign + "0." + "0" * (-exponenta_int - 1) + "1" + mantissa
        return BinaryConverter.conver_with_fixed_point(result)


class BinaryInt:
    def __init__(self, decimal: int, *, bits_number: int = 8):
        assert (
            -(2 ** (bits_number - 1) - 1) <= decimal <= 2 ** (bits_number - 1) - 1
        ), f"Your number {decimal} is not in  [-(2^({bits_number} - 1) - 1); 2^({bits_number} - 1) - 1]\n"

        self.bits_number = bits_number
        self.decimal = decimal
        self.sign_magnitude = self._get_sign_magnitude()
        self.ones_complement = self._get_ones_complement()
        self.twos_complement = self._get_twos_complement()

    @staticmethod
    def _get_binary_simple(decimal: int) -> str:
        buf_decimal = abs(decimal)
        result = ""
        while buf_decimal:
            result = str(buf_decimal % 2) + result
            buf_decimal //= 2
        return result

    def _get_binary(self) -> str:
        buf_decimal = abs(self.decimal)
        result = ""
        while buf_decimal:
            result = str(buf_decimal % 2) + result
            buf_decimal //= 2
        return (self.bits_number - len(result) - 1) * "0" + result

    def _get_sign_magnitude(self) -> str:
        if self.decimal >= 0:
            return "0" + self._get_binary()
        else:
            return "1" + self._get_binary()

    def _get_ones_complement(self) -> str:
        if self.decimal >= 0:
            return "0" + self._get_binary()
        else:
            return "1" + "".join(
                "1" if bit == "0" else "0" for bit in self._get_binary()
            )

    def _get_twos_complement(self) -> str:
        if self.decimal >= 0:
            return "0" + self._get_binary()
        else:
            return self._binary_sum(
                self.ones_complement,
                "1",
                bits_number=self.bits_number,
            )

    @staticmethod
    def _binary_sum(value1: str, value2: str, *, bits_number: int) -> str:
        result = ""
        buffer = 0
        value1, value2 = value1.zfill(bits_number), value2.zfill(bits_number)
        for i in range(-1, -bits_number - 1, -1):
            total_sum = int(value1[i]) + int(value2[i]) + buffer
            result = str(total_sum % 2) + result
            buffer = total_sum // 2
        if buffer == 1:
            result = "1" + result
        return result

    def __add__(self, other: "BinaryInt") -> "BinaryInt":
        first_summand, second_summand = self.twos_complement, other.twos_complement
        if self.bits_number > other.bits_number and other.decimal < 0:
            min_int = BinaryConverter.convert_twos_complement(second_summand)
            second_summand = BinaryInt(
                min_int, bits_number=self.bits_number
            ).twos_complement
        elif self.bits_number < other.bits_number and self.decimal < 0:
            min_int = BinaryConverter.convert_twos_complement(first_summand)
            first_summand = BinaryInt(
                min_int, bits_number=other.bits_number
            ).twos_complement
        result_bits_numer = max(len(first_summand), len(second_summand))
        result_str = BinaryInt._binary_sum(
            first_summand, second_summand, bits_number=result_bits_numer
        )
        if first_summand[0] == second_summand[0] != result_str[-result_bits_numer]:
            raise OverflowError("Oops, overflow has just happened\n")
        result_int = BinaryConverter.convert_twos_complement(
            result_str[-result_bits_numer:]
        )
        return BinaryInt(result_int, bits_number=len(result_str))

    def __sub__(self, other: "BinaryInt") -> "BinaryInt":
        return BinaryInt(-other.decimal, bits_number=other.bits_number) + self

    def __mul__(self, other: "BinaryInt") -> "BinaryInt":
        if self.decimal == 0 or other.decimal == 0:
            return BinaryInt(0)
        if self.decimal > other.decimal:
            multiplicant, multiplier = self.sign_magnitude[1:].lstrip(
                "0"
            ), other.sign_magnitude[1:].lstrip("0")
        else:
            multiplicant, multiplier = other.sign_magnitude[1:].lstrip(
                "0"
            ), self.sign_magnitude[1:].lstrip("0")
        list_of_sums = []
        for i in range(-1, -len(multiplier) - 1, -1):
            digit = multiplier[i]
            if digit == "1":
                list_of_sums.append(
                    (len(multiplier) + i) * "0" + multiplicant + (-i - 1) * "0"
                )
            else:
                list_of_sums.append("0" * (len(multiplier) + len(multiplicant) - 1))
        for i in range(1, len(list_of_sums)):
            list_of_sums[i] = BinaryInt._binary_sum(
                list_of_sums[i],
                list_of_sums[i - 1],
                bits_number=len(list_of_sums[i]),
            )

        if self.sign_magnitude[0] == other.sign_magnitude[0]:
            result_str = "0" + list_of_sums[-1]
        else:
            result_str = "1" + list_of_sums[-1]
        result_int = BinaryConverter.convert_sign_magnitude(result_str)
        return BinaryInt(result_int, bits_number=len(list_of_sums[-1]) + 1)

    def __truediv__(self, other: "BinaryInt") -> "BinaryFloatFixed":
        if other.decimal == 0:
            raise ZeroDivisionError("We can't devide on 0\n")
        if self.decimal == 0:
            return BinaryFloatFixed.create_from_str(
                "0.0", (self.decimal / other.decimal)
            )
        sign = "0" if self.decimal * other.decimal > 0 else "1"
        devidend, divisor = BinaryInt._get_binary_simple(
            self.decimal
        ), BinaryInt._get_binary_simple(other.decimal)
        remainder = ""
        result = ""

        for i in range(len(devidend)):
            remainder += devidend[i]
            if BinaryConverter.to_decimal(remainder) < BinaryConverter.to_decimal(
                divisor
            ):
                result += "0"
            else:
                result += "1"
                remainder = BinaryInt._get_binary_simple(
                    (
                        BinaryConverter.to_decimal(remainder)
                        - BinaryConverter.to_decimal(divisor)
                    )
                )
        result += "."

        if BinaryConverter.to_decimal(remainder) != 0:
            for i in range(BinaryFloatFixed.DEFAULT_ACCURACY):
                remainder += "0"
                if BinaryConverter.to_decimal(remainder) < BinaryConverter.to_decimal(
                    divisor
                ):
                    result += "0"
                else:
                    result += "1"
                    remainder = BinaryInt._get_binary_simple(
                        (
                            BinaryConverter.to_decimal(remainder)
                            - BinaryConverter.to_decimal(divisor)
                        )
                    )
        result = result.lstrip("0")
        return BinaryFloatFixed.create_from_str(
            sign + result, (self.decimal / other.decimal)
        )

    def __repr__(self):
        return f"BinaryInt({self.decimal})"

    def __str__(self):
        return (
            f"\nDecimal representation: {self.decimal}\n"
            f"Binary representation:\n"
            f"  - Sign magnitude: {self.sign_magnitude}\n"
            f"  - One's complement: {self.ones_complement}\n"
            f"  - Two's complement: {self.twos_complement}\n"
        )


class BinaryFloatFixed:
    DEFAULT_ACCURACY = 5

    def __init__(
        self,
        decimal_float: float,
        precision: int = DEFAULT_ACCURACY,
        binary_str: str = "",
    ):
        self.decimal_float = decimal_float
        self.precision = precision
        if binary_str:
            self.binary_float = binary_str
        else:
            self.binary_float = self._get_binary_fixed()

    @classmethod
    def create_from_str(cls, binary_str: str, decimal_float: float):
        return BinaryFloatFixed(decimal_float, binary_str=binary_str)

    def _get_binary_fixed(self) -> str:
        if self.decimal_float == 0:
            return "0.0"
        sign = "0" if self.decimal_float >= 0 else "1"
        decimal_float_abs = abs(self.decimal_float)

        int_part = int(decimal_float_abs)
        fractional_part = str(decimal_float_abs - int_part)
        fractional_part = float("0" + fractional_part[fractional_part.find(".") :])

        int_part_str = BinaryInt._get_binary_simple(int_part)
        fractional_part_str = ""
        i = 0
        while fractional_part > 0 and i < self.precision:
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_part_str += str(bit)
            fractional_part -= bit
            i += 1

        if not fractional_part_str:
            fractional_part_str = "0"
        else:
            fractional_part_str = fractional_part_str.rstrip("0")
        return f"{sign}{int_part_str}.{fractional_part_str}"

    def __str__(self):
        return (
            f"\nDecimal representation (before converting): {self.decimal_float}\n"
            f"Decimal representation (after converting): {BinaryConverter.conver_with_fixed_point(self.binary_float)}\n"
            f"Binary representation (with fixed point): {self.binary_float}\n"
        )


class BinaryFloatIEEE:
    EXPONENTA_LENGTH = 8
    MANTISSA_LENGTH = 23

    def __init__(
        self,
        bin_float_point: BinaryFloatFixed = None,
        sign: str = "",
        exponenta: str = "",
        mantissa: str = "",
    ):
        if sign + exponenta + mantissa:
            self.sign = sign
            self.exponenta = exponenta
            self.mantissa = mantissa
        else:
            self.sign, self.exponenta, self.mantissa = self._get_ieee_number(
                bin_float_point
            )

    @classmethod
    def create_from_sem(cls, sign: str, exponenta: str, mantissa: str):
        return BinaryFloatIEEE(sign=sign, exponenta=exponenta, mantissa=mantissa)

    def _get_ieee_number(self, number_fixed_point):
        if number_fixed_point.decimal_float == 0:
            return (
                "0",
                "0" * BinaryFloatIEEE.EXPONENTA_LENGTH,
                "0" * BinaryFloatIEEE.MANTISSA_LENGTH,
            )
        number = number_fixed_point.binary_float
        sign = number[0]
        number = number[1:].split(".")

        exponenta = 0
        mantissa = ""
        if number[0]:
            mantissa = number[0][1:] + number[1]
            exponenta = len(mantissa) - len(number[1])
        else:
            mantissa = number[1][number[1].find("1") + 1 :]
            exponenta = len(mantissa) - len(number[1])

        exponenta = BinaryInt._get_binary_simple(exponenta + 127).zfill(
            BinaryFloatIEEE.EXPONENTA_LENGTH
        )
        mantissa = mantissa.ljust(BinaryFloatIEEE.MANTISSA_LENGTH, "0")[:23]
        return (sign, exponenta, mantissa)

    def __add__(self, other: "BinaryFloatIEEE") -> "BinaryFloatIEEE":
        if self.sign != other.sign:
            raise Exception(
                "Unfortunately this program can't add numbers with different sign yet\n"
            )
        result_sign = self.sign

        result_exponenta = max(self.exponenta, other.exponenta)
        if self.exponenta == other.exponenta:
            result_mantissa = BinaryInt._binary_sum(
                other.mantissa,
                self.mantissa,
                bits_number=BinaryFloatIEEE.MANTISSA_LENGTH,
            )
            result_exponenta = BinaryInt._get_binary_simple(
                BinaryConverter.to_decimal(result_exponenta) + 1
            ).zfill(BinaryFloatIEEE.EXPONENTA_LENGTH)
            if len(result_mantissa) > BinaryFloatIEEE.MANTISSA_LENGTH:
                result_mantissa = (result_mantissa)[:23]
            else:
                result_mantissa = ("0" + result_mantissa)[:23]
        else:
            exp_dif = abs(
                BinaryConverter.to_decimal((self.exponenta))
                - BinaryConverter.to_decimal(other.exponenta)
            )
            if self.exponenta > other.exponenta:
                edited_mantissa = ("0" * (exp_dif - 1) + "1" + other.mantissa)[
                    : BinaryFloatIEEE.MANTISSA_LENGTH
                ]
                result_mantissa = BinaryInt._binary_sum(
                    self.mantissa,
                    edited_mantissa,
                    bits_number=BinaryFloatIEEE.MANTISSA_LENGTH,
                )
            else:
                edited_mantissa = ("0" * (exp_dif - 1) + "1" + self.mantissa)[
                    : BinaryFloatIEEE.MANTISSA_LENGTH
                ]
                result_mantissa = BinaryInt._binary_sum(
                    other.mantissa,
                    edited_mantissa,
                    bits_number=BinaryFloatIEEE.MANTISSA_LENGTH,
                )
            if len(result_mantissa) > BinaryFloatIEEE.MANTISSA_LENGTH:
                result_exponenta = BinaryInt._get_binary_simple(
                    BinaryConverter.to_decimal(result_exponenta) + 1
                ).zfill(BinaryFloatIEEE.EXPONENTA_LENGTH)
                result_mantissa = ("0" + result_mantissa[1:])[:23]

        return BinaryFloatIEEE.create_from_sem(
            result_sign, result_exponenta, result_mantissa
        )

    def __str__(self):
        return (
            f"Decimal representation (after converting): {BinaryConverter.convert_ieee(self.sign, self.exponenta, self.mantissa)}\n"
            f"Binary representation (IEEE-754): {self.sign}_{self.exponenta}_{self.mantissa}\n"
        )


# rand_float_bin_1 = BinaryFloatFixed(-11, precision=32)
# print(rand_float_bin_1)
# rand_float_bin_2 = BinaryFloatFixed(-11, precision=32)
# print(rand_float_bin_2)
# first_ieee = BinaryFloatIEEE(rand_float_bin_1)
# print(first_ieee)
# second_ieee = BinaryFloatIEEE(rand_float_bin_2)
# print(second_ieee)

# result_ieee = first_ieee + second_ieee
# print(result_ieee)
