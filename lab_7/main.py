from src.diagonal_matrix import DiagonalMatrix


def print_menu():
    print("\n===== Главное меню =====")
    print("1. Работа со словами и диагоналями")
    print("2. Логические операции")
    print("3. Сложение полей")
    print("4. Поиск в интервале")
    print("0. Выход")
    return input("Выбор: ")


def handle_read_write(matrix):
    while True:
        print("\n1. Просмотр матрицы")
        print("2. Считать слово")
        print("3. Записать слово")
        print("4. Считать диагональ")
        print("5. Записать диагональ")
        print("0. Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break
        elif choice == "1":
            matrix.print()
        elif choice == "2":
            try:
                index = int(input("Индекс слова (0-15): "))
                if 0 <= index < matrix.size:
                    print(f"Слово {index}: {matrix.find_word(index)}")
            except ValueError:
                print("Ошибка: введите число")
        elif choice == "3":
            try:
                index = int(input("Индекс слова (0-15): "))
                if 0 <= index < matrix.size:
                    bits = [int(bit) for bit in input("Биты (через пробел): ").split()]
                    if len(bits) == matrix.size and all(bit in [0, 1] for bit in bits):
                        matrix.change_word(index, bits)
                        print("Слово изменено")
            except ValueError:
                print("Ошибка: введите числа")
        elif choice == "4":
            try:
                index = int(input("Индекс диагонали (0-15): "))
                if 0 <= index < matrix.size:
                    print(f"Диагональ {index}: {matrix.find_diagonal(index)}")
            except ValueError:
                print("Ошибка: введите число")
        elif choice == "5":
            try:
                index = int(input("Индекс диагонали (0-15): "))
                if 0 <= index < matrix.size:
                    bits = [int(bit) for bit in input("Биты (через пробел): ").split()]
                    if len(bits) == matrix.size and all(bit in [0, 1] for bit in bits):
                        matrix.change_diagonal(index, bits)
                        print("Диагональ изменена")
            except ValueError:
                print("Ошибка: введите числа")


def handle_logical_operations(matrix):
    while True:
        print("\n1. Запрет (a & !b)")
        print("2. Дизъюнкция (a | b)")
        print("3. Пирс !(a | b)")
        print("4. Импликация (a -> b)")
        print("0. Назад")

        choice = input("Выбор: ")

        if choice == "0":
            break

        if choice in ["1", "2", "3", "4"]:
            try:
                idx1 = int(input("Индекс 1-го слова: "))
                idx2 = int(input("Индекс 2-го слова: "))
                res_idx = int(input("Индекс результата: "))

                if all(0 <= idx < matrix.size for idx in [idx1, idx2, res_idx]):
                    word1 = matrix.find_word(idx1)
                    word2 = matrix.find_word(idx2)

                    operations = {
                        "1": (matrix.inhibition, "Запрет"),
                        "2": (matrix.disjunction, "Дизъюнкция"),
                        "3": (matrix.peirce, "Пирс"),
                        "4": (matrix.implication, "Импликация"),
                    }

                    op_func, op_name = operations[choice]
                    result = op_func(word1, word2)
                    matrix.change_word(res_idx, result)
                    print(f"{op_name}: {result}")
            except ValueError:
                print("Ошибка: введите числа")


def handle_add_fields(matrix):
    print("\n===== Сложение полей =====")
    try:
        key_input = input("Введите ключ (3 бита через пробел, например: 1 0 1): ")
        key = [int(bit) for bit in key_input.split()]

        if len(key) == 3 and all(bit in [0, 1] for bit in key):
            print("\nИсходная матрица:")
            matrix.print()

            # Запоминаем слова до операции
            original_words = [matrix.find_word(i) for i in range(matrix.size)]

            matrix.add_fields(key)

            print(f"\nМатрица после сложения полей с ключом {key}:")
            matrix.print()

            # Находим измененные слова
            modified_indices = []
            for i in range(matrix.size):
                if matrix.find_word(i) != original_words[i]:
                    modified_indices.append(i)

            if modified_indices:
                print("\nИзмененные слова (индексы):", modified_indices)
                print("\nДетали изменений:")
                for idx in modified_indices:
                    print(f"Слово {idx}:")
                    print(f"  До:    {original_words[idx]}")
                    print(f"  После: {matrix.find_word(idx)}")
            else:
                print("\nНи одно слово не было изменено (нет соответствий ключу)")
        else:
            print("Ключ должен состоять ровно из 3 бит (0 или 1)")
    except ValueError:
        print("Ошибка: введите целые числа 0 или 1, разделенные пробелами")


def handle_interval_search(matrix):
    try:
        start = int(input("Начало поля (0-15): "))
        end = int(input("Конец поля (0-15): "))
        lower = int(input("Нижняя граница: "))
        upper = int(input("Верхняя граница: "))

        if 0 <= start <= end < matrix.size and lower <= upper:
            matches = matrix.search_interval(lower, upper, (start, end))
            if matches:
                print(f"Найдены слова: {matches}")
            else:
                print("Слова не найдены")
        else:
            print("Неверные границы")
    except ValueError:
        print("Ошибка: введите числа")


def main():
    matrix = DiagonalMatrix()
    print("Создана матрица 16x16")
    matrix.print()

    while True:
        choice = print_menu()

        if choice == "0":
            break
        elif choice == "1":
            handle_read_write(matrix)
        elif choice == "2":
            handle_logical_operations(matrix)
        elif choice == "3":
            handle_add_fields(matrix)
        elif choice == "4":
            handle_interval_search(matrix)
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
