from pnf_contructor.truth_table import TruthTable
from pnf_contructor.logical_function import LogicalFunction
from corno.computational import Minimizer


while True:
    function_str = input("fun> ")

    if function_str == "exit":
        break
    elif not function_str:
        continue

    function = LogicalFunction(function_str)
    table = TruthTable(function)
    table.display()
    print(end="\n---------------------------------------\n")
    minimizer = Minimizer(table)
    result1 = minimizer.computational_table_minimization(is_pdnf=False)
    print("CNF: ", result1, end="\n---------------------------------------\n")
    result2 = minimizer.computational_table_minimization(is_pdnf=True)
    print("DNF: ", result2)
    print(end="\n---------------------------------------\n")
    result3 = minimizer.computational_minimization(is_pdnf=False)
    print("CNF: ", result3, end="\n---------------------------------------\n")
    result4 = minimizer.computational_minimization(is_pdnf=True)
    print("DNF: ", result4, end="\n---------------------------------------\n")

    result5 = minimizer.karnaugh_map_minimization(is_pdnf=False)
