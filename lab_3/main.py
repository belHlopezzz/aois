from src.pnf_contructor.truth_table import TruthTable
from src.pnf_contructor.logical_function import LogicalFunction
from src.corno.minimizer import Minimizer
from colorama import init, Fore, Style

# Initialize colorama
init()


def print_header():
    print("\n" + "=" * 80)
    print(
        Fore.GREEN
        + "Logical Function Minimization Program".center(80)
        + Style.RESET_ALL
    )
    print("=" * 80)
    print("\nThis program can minimize logical functions using three methods:")
    print("1. Quine-McCluskey method (computational method)")
    print("2. Quine-McCluskey method with coverage table")
    print("3. Karnaugh map method")
    print("\nType 'exit' to quit")
    print("-" * 80 + "\n")


def print_minimization_results(minimizer: Minimizer, function_str: str):
    print("\n" + "=" * 80)
    print(
        Fore.GREEN
        + f"Minimization results for function: {function_str}"
        + Style.RESET_ALL
    )
    print("=" * 80)

    print("\n" + Fore.GREEN + "1. Perfect Normal Forms:" + Style.RESET_ALL)
    print("-" * 40)
    print(
        Fore.YELLOW + "PCNF:" + Style.RESET_ALL,
        minimizer.truth_table.get_pcnf(),
        end="\n\n",
    )
    print(Fore.YELLOW + "PDNF:" + Style.RESET_ALL, minimizer.truth_table.get_pdnf())
    print("-" * 40)

    print("\n" + Fore.GREEN + "2. Minimization Results:" + Style.RESET_ALL)
    print("-" * 40)

    print("\n" + Fore.GREEN + "Computational Method:" + Style.RESET_ALL)
    print(
        Fore.YELLOW + "CNF:" + Style.RESET_ALL,
        minimizer.computational_minimization(is_pdnf=False),
        end="\n\n",
    )
    print(
        Fore.YELLOW + "DNF:" + Style.RESET_ALL,
        minimizer.computational_minimization(is_pdnf=True),
    )

    print("\n" + Fore.GREEN + "Computational Table Method:" + Style.RESET_ALL)
    print(
        Fore.YELLOW + "CNF:" + Style.RESET_ALL,
        minimizer.computational_table_minimization(is_pdnf=False),
    )
    print(
        Fore.YELLOW + "DNF:" + Style.RESET_ALL,
        minimizer.computational_table_minimization(is_pdnf=True),
    )

    print("\n" + Fore.GREEN + "Karnaugh Map Method:" + Style.RESET_ALL)
    print(
        Fore.YELLOW + "CNF:" + Style.RESET_ALL,
        minimizer.karnaugh_map_minimization(is_pdnf=False),
    )
    print(
        Fore.YELLOW + "DNF:" + Style.RESET_ALL,
        minimizer.karnaugh_map_minimization(is_pdnf=True),
    )
    print("-" * 40)


def main():
    print_header()

    while True:
        function_str = input("\nEnter logical expression> ")

        if function_str.lower() == "exit":
            print(
                "\n" + Fore.GREEN + "Thank you for using the program!" + Style.RESET_ALL
            )
            break
        elif not function_str:
            continue

        try:
            function = LogicalFunction(function_str)
            table = TruthTable(function)
            minimizer = Minimizer(table)

            print_minimization_results(minimizer, function_str)

        except Exception as e:
            print(f"\n" + Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)
            print("Please check the correctness of the entered expression.")


if __name__ == "__main__":
    main()
