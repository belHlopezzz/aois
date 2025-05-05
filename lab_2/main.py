from logical_function import LogicalFunction
from truth_table import TruthTable

def main():
    print("Logical Formula Truth Table Generator")
    print("Operators: !, &, |, >, ~")
    print("Variables: Single letters (a-z, A-Z)")
    print("Example: (a & b) | !c")
    print("Enter 'exit' to quit.")

    while True:
        text = input("\nEnter formula: ")

        if not text:
            continue
        if text.lower() == "exit":
            break

        try:
            logical_function = LogicalFunction(text)

            table = TruthTable(logical_function)
            table.display()
        except Exception as e:
            print(e)

    print("\nExiting program.")


if __name__ == "__main__":
    main()