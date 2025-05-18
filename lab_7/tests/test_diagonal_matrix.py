import pytest
from diagonal_matrix import DiagonalMatrix
import random


class TestDiagonalMatrix:
    def test_init_default(self):
        matrix = DiagonalMatrix()
        assert matrix.size == 16
        assert len(matrix.matrix) == 16
        assert all(len(row) == 16 for row in matrix.matrix)
        assert all(all(bit in [0, 1] for bit in row) for row in matrix.matrix)
        assert len(matrix.g_flags) == 16
        assert len(matrix.l_flags) == 16
        assert len(matrix.result_flags) == 16

    def test_init_custom_size(self):
        size = 8
        matrix = DiagonalMatrix(size=size)
        assert matrix.size == size
        assert len(matrix.matrix) == size
        assert all(len(row) == size for row in matrix.matrix)

    def test_init_provided_matrix(self):
        test_matrix = [[1, 0], [0, 1]]
        matrix = DiagonalMatrix(size=2, matrix=test_matrix)
        assert matrix.size == 2
        assert matrix.matrix == test_matrix

    def test_init_validation(self):
        test_matrix = [[1, 0], [0, 1]]
        with pytest.raises(ValueError):
            DiagonalMatrix(size=3, matrix=test_matrix)

        test_matrix = [[1, 0, 1], [0, 1]]
        with pytest.raises(ValueError):
            DiagonalMatrix(size=2, matrix=test_matrix)

    def test_generate_random_matrix(self):
        original_randint = random.randint
        random.randint = lambda a, b: 1

        matrix = DiagonalMatrix(size=4)
        assert all(all(bit == 1 for bit in row) for row in matrix.matrix)

        random.randint = original_randint

    def test_get_column(self):
        test_matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        matrix = DiagonalMatrix(size=3, matrix=test_matrix)

        column = matrix.get_column(1)
        assert column == [0, 1, 1]

    def test_find_word(self):
        test_matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        matrix = DiagonalMatrix(size=3, matrix=test_matrix)

        word = matrix.find_word(1)
        assert word == [1, 1, 0]

    def test_change_word(self):
        test_matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        matrix = DiagonalMatrix(size=3, matrix=test_matrix)

        new_word = [0, 0, 0]
        matrix.change_word(1, new_word)

        assert matrix.get_column(1) == [0, 0, 0]
        assert matrix.find_word(1) == [0, 0, 0]

    def test_change_word_validation(self):
        matrix = DiagonalMatrix(size=3)

        with pytest.raises(ValueError):
            matrix.change_word(1, [0, 0])

    def test_find_diagonal(self):
        test_matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        matrix = DiagonalMatrix(size=3, matrix=test_matrix)

        diagonal = matrix.find_diagonal(0)
        assert diagonal == [1, 1, 0]

        diagonal = matrix.find_diagonal(1)
        assert diagonal == [0, 1, 1]

    def test_change_diagonal(self):
        test_matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 0]]
        matrix = DiagonalMatrix(size=3, matrix=test_matrix)

        new_diagonal = [0, 0, 0]
        matrix.change_diagonal(0, new_diagonal)

        assert matrix.find_diagonal(0) == [0, 0, 0]

        assert matrix.matrix[0][0] == 0
        assert matrix.matrix[1][1] == 0
        assert matrix.matrix[2][2] == 0

    def test_change_diagonal_validation(self):
        matrix = DiagonalMatrix(size=3)

        with pytest.raises(ValueError):
            matrix.change_diagonal(1, [0, 0])

    def test_inhibition(self):
        a = [1, 0, 1, 0]
        b = [0, 0, 1, 1]

        result = DiagonalMatrix.inhibition(a, b)
        assert result == [1, 0, 0, 0]

    def test_disjunction(self):
        a = [1, 0, 1, 0]
        b = [0, 0, 1, 1]

        result = DiagonalMatrix.disjunction(a, b)
        assert result == [1, 0, 1, 1]

    def test_peirce(self):
        a = [1, 0, 1, 0]
        b = [0, 0, 1, 1]

        result = DiagonalMatrix.peirce(a, b)
        assert result == [0, 1, 0, 0]

    def test_implication(self):
        a = [1, 0, 1, 0]
        b = [0, 0, 1, 1]

        result = DiagonalMatrix.implication(a, b)
        assert result == [0, 1, 1, 1]

    def test_logical_operations_validation(self):
        a = [1, 0, 1]
        b = [0, 0]

        operations = [
            DiagonalMatrix.inhibition,
            DiagonalMatrix.disjunction,
            DiagonalMatrix.peirce,
            DiagonalMatrix.implication,
        ]

        for op in operations:
            with pytest.raises(ValueError):
                op(a, b)

    def test_add_fields(self):
        test_matrix = [[0 for _ in range(16)] for _ in range(16)]

        column_idx = 5
        for i in range(16):
            test_matrix[i][column_idx] = 0

        test_matrix[5][column_idx] = 1
        test_matrix[6][column_idx] = 0
        test_matrix[7][column_idx] = 1

        test_matrix[8][column_idx] = 1
        test_matrix[9][column_idx] = 0
        test_matrix[10][column_idx] = 1
        test_matrix[11][column_idx] = 0

        test_matrix[12][column_idx] = 0
        test_matrix[13][column_idx] = 1
        test_matrix[14][column_idx] = 0
        test_matrix[15][column_idx] = 1

        matrix = DiagonalMatrix(size=16, matrix=test_matrix)

        matrix.add_fields([1, 0, 1])

        word = matrix.find_word(column_idx)

        assert word[:11] == [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1]
        assert word[11:16] == [0, 1, 1, 1, 1]

    def test_add_fields_with_carry(self):
        test_matrix = [[0 for _ in range(16)] for _ in range(16)]

        column_idx = 3

        test_matrix[3][column_idx] = 1
        test_matrix[4][column_idx] = 1
        test_matrix[5][column_idx] = 0

        test_matrix[6][column_idx] = 1
        test_matrix[7][column_idx] = 1
        test_matrix[8][column_idx] = 1
        test_matrix[9][column_idx] = 1

        test_matrix[10][column_idx] = 0
        test_matrix[11][column_idx] = 0
        test_matrix[12][column_idx] = 0
        test_matrix[13][column_idx] = 1

        matrix = DiagonalMatrix(size=16, matrix=test_matrix)

        matrix.add_fields([1, 1, 0])

        word = matrix.find_word(column_idx)

        assert word[14:] == [0, 0]

    def test_add_fields_validation(self):
        matrix = DiagonalMatrix()

        with pytest.raises(ValueError):
            matrix.add_fields([1, 0])

    def test_initialize_result_flags(self):
        matrix = DiagonalMatrix(size=4)

        matrix.result_flags = [0, 0, 0, 0]

        matrix.initialize_result_flags()
        assert matrix.result_flags == [1, 1, 1, 1]

    def test_perform_comparison(self):
        test_matrix = [[1, 0, 0, 1], [0, 1, 0, 0], [1, 0, 1, 0], [1, 1, 0, 1]]
        matrix = DiagonalMatrix(size=4, matrix=test_matrix)

        matrix.perform_comparison([1, 0], (1, 2))

        assert matrix.g_flags == [0, 0, 0, 0]
        assert matrix.l_flags == [1, 1, 1, 0]

    def test_perform_comparison_validation(self):
        matrix = DiagonalMatrix(size=4)

        with pytest.raises(ValueError):
            matrix.perform_comparison([1, 0, 1], (1, 2))

    def test_apply_less_than_condition(self):
        matrix = DiagonalMatrix(size=4)

        matrix.result_flags = [1, 1, 1, 1]
        matrix.g_flags = [1, 0, 0, 1]
        matrix.l_flags = [0, 1, 0, 0]

        matrix.apply_less_than_condition()

        assert matrix.result_flags == [0, 1, 0, 0]

    def test_apply_greater_than_condition(self):
        matrix = DiagonalMatrix(size=4)

        matrix.result_flags = [1, 1, 1, 1]
        matrix.g_flags = [1, 0, 0, 1]

        matrix.apply_greater_than_condition()

        assert matrix.result_flags == [1, 0, 0, 1]

    def test_search_interval(self):
        test_matrix = [[0 for _ in range(4)] for _ in range(4)]

        test_matrix[0][0] = 0
        test_matrix[1][0] = 0

        test_matrix[0][1] = 0
        test_matrix[1][1] = 1

        test_matrix[0][2] = 1
        test_matrix[1][2] = 0

        test_matrix[0][3] = 1
        test_matrix[1][3] = 1

        matrix = DiagonalMatrix(size=4, matrix=test_matrix)

        result = matrix.search_interval(1, 2, (0, 1))
        assert sorted(result) == []

        result = matrix.search_interval(0, 3, (0, 1))
        assert sorted(result) == [1, 3]
