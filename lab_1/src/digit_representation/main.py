from binary_data_types import *


class Menu:
    def __init__(self):
        is_woking = True
        while is_woking:
            choice = int(
                input(
                    "Choose operation:\n1.Get direct, reverse binary, additional binary\n2.Get binary with fixed point\n3.Get binary with floating point (IEEE)\n4.Get sum of additional binary\n5.Get subtraction of additional binary\n6.Get multiplication of direct binary\n7.Divide binary\n8.Get sum of binary with floating point\nEnter your choice (1-8, or any other number to exit):\t"
                )
            )
            if choice == 1:
                try:
                    print()
                    value, bits_number = int(input("Enter value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    binary_int_repr = BinaryInt(value, bits_number=bits_number)
                    print(binary_int_repr)
                except AssertionError as e:
                    print(f"{e}")
                except ValueError:
                    print("Value and bits number must be a number\n")
            elif choice == 2:
                try:
                    print()
                    value, precision = float(input("Enter value:\t")), int(
                        input("Enter precision:\t")
                    )
                    binary_float_repr = BinaryFloatFixed(value, precision=precision)
                    print(binary_float_repr)
                except ValueError:
                    print("Value must be any number and precision must be int number\n")
            elif choice == 3:
                try:
                    print()
                    value = float(input("Enter value:\t"))
                    binary_float_repr = BinaryFloatFixed(value, precision=25)
                    binary_float_repr_ieee = BinaryFloatIEEE(binary_float_repr)
                    print(binary_float_repr_ieee)
                except ValueError:
                    print("Value must be any number\n")
            elif choice == 4:
                try:
                    print()
                    value1, bits_number1 = int(input("Enter first value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    value2, bits_number2 = int(input("Enter second value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    binary_int_repr1 = BinaryInt(value1, bits_number=bits_number1)
                    binary_int_repr2 = BinaryInt(value2, bits_number=bits_number2)
                    print(binary_int_repr1)
                    print(binary_int_repr2)
                    print("Result:\t", binary_int_repr1 + binary_int_repr2)
                except AssertionError as e:
                    print(f"{e}")
                except ValueError:
                    print("Value and bits number must be a number\n")
                except OverflowError as e:
                    print(f"{e}")
            elif choice == 5:
                try:
                    print()
                    value1, bits_number1 = int(input("Enter first value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    value2, bits_number2 = int(input("Enter second value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    binary_int_repr1 = BinaryInt(value1, bits_number=bits_number1)
                    binary_int_repr2 = BinaryInt(value2, bits_number=bits_number2)
                    print(binary_int_repr1)
                    print(binary_int_repr2)
                    print("Result:\t", binary_int_repr1 - binary_int_repr2)
                except AssertionError as e:
                    print(f"{e}")
                except ValueError:
                    print("Value and bits number must be a number\n")
                except OverflowError as e:
                    print(f"{e}")
            elif choice == 6:
                try:
                    print()
                    value1, bits_number1 = int(input("Enter first value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    value2, bits_number2 = int(input("Enter second value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    binary_int_repr1 = BinaryInt(value1, bits_number=bits_number1)
                    binary_int_repr2 = BinaryInt(value2, bits_number=bits_number2)
                    print(binary_int_repr1)
                    print(binary_int_repr2)
                    print("Result:\t", binary_int_repr1 * binary_int_repr2)
                except AssertionError as e:
                    print(f"{e}")
                except ValueError:
                    print("Value and bits number must be a number\n")
            elif choice == 7:
                try:
                    print()
                    value1, bits_number1 = int(input("Enter first value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    value2, bits_number2 = int(input("Enter second value:\t")), int(
                        input("Enter bits number:\t")
                    )
                    binary_int_repr1 = BinaryInt(value1, bits_number=bits_number1)
                    binary_int_repr2 = BinaryInt(value2, bits_number=bits_number2)
                    print(binary_int_repr1)
                    print(binary_int_repr2)
                    print("Result:\t", binary_int_repr1 / binary_int_repr2)
                except AssertionError as e:
                    print(f"{e}")
                except ValueError:
                    print("Value and bits number must be a number\n")
                except ZeroDivisionError as e:
                    print(f"{e}")
            elif choice == 8:
                try:
                    print()
                    value1 = float(input("Enter first value:\t"))
                    value2 = float(input("Enter second value:\t"))
                    binary_float_repr1 = BinaryFloatFixed(value1, precision=25)
                    binary_float_repr_ieee1 = BinaryFloatIEEE(binary_float_repr1)
                    binary_float_repr2 = BinaryFloatFixed(value2, precision=25)
                    binary_float_repr_ieee2 = BinaryFloatIEEE(binary_float_repr2)
                    print(binary_float_repr_ieee1)
                    print(binary_float_repr_ieee2)
                    print(binary_float_repr_ieee1 + binary_float_repr_ieee2)
                except ValueError:
                    print("Value must be any number\n")
                except Exception as e:
                    print(f"{e}")
            else:
                is_woking = False


if __name__ == "__main__":
    programm_menu = Menu()
