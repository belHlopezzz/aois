from colorama import Fore, Back, Style, init
import time

from src.table_truth_generator.logical_function import LogicalFunction
from src.table_truth_generator.truth_table import TruthTable


def main():
    init()

    print(Fore.GREEN + Style.BRIGHT + "Logical Formula Truth Table Generator" + Style.RESET_ALL)
    print(Fore.WHITE + "Operators: ! (NOT), & (AND), | (OR), > (IMP), ~ (EQU)" + Style.RESET_ALL)
    print(Fore.WHITE + "Variables: Single letters (a-z, A-Z)" + Style.RESET_ALL)
    print(Fore.WHITE + "Example: (a & b) | !c" + Style.RESET_ALL)
    print(Fore.WHITE + "Enter 'exit' to quit." + Style.RESET_ALL)
    print(Fore.WHITE + "Note: Formulas with more than 10 variables may have limited index form output." + Style.RESET_ALL)

    while True:
        text = input(Fore.YELLOW + "\nEnter formula: " + Style.RESET_ALL)

        if not text:
            print(Fore.RED + "Error: Empty input. Please enter a formula." + Style.RESET_ALL)
            continue
        if text.lower() == "exit":
            break

        try:
            start_time = time.perf_counter()

            logical_function = LogicalFunction(text)

            if len(logical_function.variables) > 10:
                print(Fore.YELLOW + "Warning: Formula has more than 10 variables. Index form will be shown as binary string only." + Style.RESET_ALL)

            print(Fore.MAGENTA + "\nTruth Table:" + Style.RESET_ALL)
            table = TruthTable(logical_function)
            table.display()

            print(Fore.BLUE + Style.BRIGHT + "PCNF: " + Style.RESET_ALL + table.get_pcnf())
            print(Fore.YELLOW + Style.BRIGHT + "PDNF: " + Style.RESET_ALL + table.get_pdnf())

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(Fore.CYAN + f"Processing time: {elapsed_time:.4f} seconds" + Style.RESET_ALL)

            print(Fore.GREEN + Style.BRIGHT + "Numeric form of PCNF: " + Style.RESET_ALL + table.get_num_form_pcnf())
            print(Fore.GREEN + Style.BRIGHT + "Numeric form of PDNF: " + Style.RESET_ALL + table.get_num_form_pdnf())

            index_form = table.get_index_form()
            if len(logical_function.variables) <= 10:
                print(Fore.MAGENTA + Style.BRIGHT + "Index form: " + Style.RESET_ALL + f"{int(index_form, 2)} - {index_form}")
            else:
                print(Fore.MAGENTA + Style.BRIGHT + "Index form (binary): " + Style.RESET_ALL + index_form)

        except Exception as e:
            print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

    print(Fore.CYAN + "\nExiting program." + Style.RESET_ALL)


if __name__ == "__main__":
    main()