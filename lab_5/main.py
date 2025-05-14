from logic.table_truth.truth_table import TruthTable
from logic.minimizer import Minimizer

table = [
    # q4 q3 q2 q1 V h4 h3 h2 h1
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1],
]


def main():
    h4_table_truth = TruthTable(table=list(map(lambda x: x[:6], table)), variables=["q4", "q3", "q2", "q1", "V"])
    h4_minimizer = Minimizer(h4_table_truth)
    print(h4_minimizer.karnaugh_map_minimization(is_pdnf=True, display_karnaugh_map=False))

    h3_table_truth = TruthTable(table=list(map(lambda x: x[:5] + [x[6]], table)), variables=["q4", "q3", "q2", "q1", "V"])
    h3_minimizer = Minimizer(h3_table_truth)
    print(h3_minimizer.karnaugh_map_minimization(is_pdnf=True, display_karnaugh_map=False))

    h2_table_truth = TruthTable(table=list(map(lambda x: x[:5] + [x[7]], table)), variables=["q4", "q3", "q2", "q1", "V"])
    h2_minimizer = Minimizer(h2_table_truth)
    print(h2_minimizer.karnaugh_map_minimization(is_pdnf=True, display_karnaugh_map=False))

    h1_table_truth = TruthTable(table=list(map(lambda x: x[:5] + [x[8]], table)), variables=["q4", "q3", "q2", "q1", "V"])
    h1_minimizer = Minimizer(h1_table_truth)
    print(h1_minimizer.karnaugh_map_minimization(is_pdnf=True, display_karnaugh_map=False))
    
if __name__ == "__main__":
    main()
