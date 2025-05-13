from logic.table_truth.truth_table import TruthTable
from logic.table_truth.logical_function import LogicalFunction
from logic.minimizer import Minimizer

ODS_SUM_TRUTH_TABLE = [
    # A, B, C, S
    [0, 0, 0, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 1, 0, 0],
    [1, 1, 1, 1],
]

ODS_CARRY_OUT_TRUTH_TABLE = [
    # A, B, C, P
    [0, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
]

D8421_PLUS_9_TRUTH_TABLE = [
    # A, B, C, D, A', B', C', D'
    [0, 0, 0, 0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],  
    [1, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0]
]

def main():
    sum_truth_table = TruthTable(table=ODS_SUM_TRUTH_TABLE, variables=["A", "B", "C"])
    print("Sum Truth Table:")
    sum_truth_table.display()
    sum_pcnf = sum_truth_table.get_pcnf()
    print("Sum PCNF: ", sum_pcnf)

    sum_pcnf_logical_function = LogicalFunction(sum_pcnf)
    sum_pcnf_truth_table = TruthTable(logical_function=sum_pcnf_logical_function)
    minimized_sum_pcnf = Minimizer(sum_pcnf_truth_table).karnaugh_map_minimization(
        is_pdnf=False, display_karnaugh_map=False
    )
    print("Minimized Sum PCNF: ", minimized_sum_pcnf)

    print("------------------------------------------------------")

    carry_out_truth_table = TruthTable(
        table=ODS_CARRY_OUT_TRUTH_TABLE, variables=["A", "B", "C"]
    )
    print("Carry Out Truth Table:")
    carry_out_truth_table.display()
    carry_out_pcnf = carry_out_truth_table.get_pcnf()
    print("Carry Out PCNF: ", carry_out_pcnf)

    carry_out_pcnf_logical_function = LogicalFunction(carry_out_pcnf)
    carry_out_pcnf_truth_table = TruthTable(
        logical_function=carry_out_pcnf_logical_function
    )
    minimized_carry_out_pcnf = Minimizer(
        carry_out_pcnf_truth_table
    ).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=False)
    print("Minimized Carry Out PCNF: ", minimized_carry_out_pcnf)

    print("------------------------------------------------------")

    d8421_plus_9_truth_table_a = TruthTable(
        table=list(map(lambda x: x[:4] + [x[4]], D8421_PLUS_9_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_9_pcnf_a = Minimizer(d8421_plus_9_truth_table_a).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=False)
    print("Minimized D8421 Plus 9 PCNF A: ", minimized_d8421_plus_9_pcnf_a, end="\n\n")
    

    d8421_plus_9_truth_table_b = TruthTable(
        table=list(map(lambda x: x[:4] + [x[5]], D8421_PLUS_9_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )   
    minimized_d8421_plus_9_pcnf_b = Minimizer(d8421_plus_9_truth_table_b).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=False)
    print("Minimized D8421 Plus 9 PCNF B: ", minimized_d8421_plus_9_pcnf_b, end="\n\n")


    d8421_plus_9_truth_table_c = TruthTable(
        table=list(map(lambda x: x[:4] + [x[6]], D8421_PLUS_9_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_9_pcnf_c = Minimizer(d8421_plus_9_truth_table_c).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=False)
    print("Minimized D8421 Plus 9 PCNF C: ", minimized_d8421_plus_9_pcnf_c, end="\n\n")


    d8421_plus_9_truth_table_d = TruthTable(
        table=list(map(lambda x: x[:4] + [x[7]], D8421_PLUS_9_TRUTH_TABLE)), variables=["A", "B", "C", "D"]
    )
    minimized_d8421_plus_9_pcnf_d = Minimizer(d8421_plus_9_truth_table_d).karnaugh_map_minimization(is_pdnf=False, display_karnaugh_map=False)
    print("Minimized D8421 Plus 9 PCNF D: ", minimized_d8421_plus_9_pcnf_d, end="\n\n")


if __name__ == "__main__":
    main()
