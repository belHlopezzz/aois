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

        # try:
        logical_function = LogicalFunction(text)

        table = TruthTable(logical_function)
        table.display()
        print("PCNF: ", table.get_pcnf(), end="\n\n")
        print("PDNF: ", table.get_pdnf(), end="\n\n")
        print("Numeric form of PCNF: ", table.get_num_form_pcnf(), end="\n\n")
        print("Numeric form of PDNF: ", table.get_num_form_pdnf(), end="\n\n")
        index_form = table.get_index_form()
        print("Index form:", int(index_form, 2), " - ", index_form)

    print("\nExiting program.")


if __name__ == "__main__":
    main()