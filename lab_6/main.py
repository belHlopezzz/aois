"""
Задание: Разрешение коллизий с помощью цепочек: сбалансированное дерево
"""

from src.hash_table import HashTable, BLANK
from colorama import init, Fore, Style


init()


def print_header(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}")


def print_success(text):
    print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")


def print_error(text):
    print(f"{Fore.RED}{text}{Style.RESET_ALL}")


def print_info(text):
    print(f"{Fore.YELLOW}{text}{Style.RESET_ALL}")


def main():
    hash_table = HashTable(10)

    books = [
        ("Война и мир", "Л.Н. Толстой"),
        ("Евгений Онегин", "А.С. Пушкин"),
        ("Преступление и наказание", "Ф.М. Достоевский"),
        ("Мертвые души", "Н.В. Гоголь"),
        ("Мастер и Маргарита", "М.А. Булгаков"),
        ("Идиот", "Ф.М. Достоевский"),
        ("Отцы и дети", "И.С. Тургенев"),
        ("Герой нашего времени", "М.Ю. Лермонтов"),
        ("Анна Каренина", "Л.Н. Толстой"),
        ("Капитанская дочка", "А.С. Пушкин"),
        ("Ревизор", "Н.В. Гоголь"),
        ("Вишневый сад", "А.П. Чехов"),
        ("Обломов", "И.А. Гончаров"),
        ("Тихий Дон", "М.А. Шолохов"),
        ("Братья Карамазовы", "Ф.М. Достоевский"),
        ("Горе от ума", "А.С. Грибоедов"),
        ("Палата №6", "А.П. Чехов"),
        ("Бесы", "Ф.М. Достоевский"),
    ]

    print(
        f"\n{Fore.MAGENTA}{Style.BRIGHT}=== ДЕМОНСТРАЦИЯ РАБОТЫ ХЕШ-ТАБЛИЦЫ С РАЗРЕШЕНИЕМ КОЛЛИЗИЙ ЧЕРЕЗ АВЛ-ДЕРЕВО ==={Style.RESET_ALL}\n"
    )

    print_header("1. Добавление элементов в хеш-таблицу:")
    for title, author in books:
        hash_table[title] = author
        hash_value = hash_table._hash_function(title)
        print_success(f"Добавлен элемент: '{title}' -> '{author}' (хеш: {hash_value})")

    print_header("\n2. Информация о хеш-таблице:")
    print_info(str(hash_table))

    print_header("\n3. Поиск элементов:")
    search_titles = ["Война и мир", "Мастер и Маргарита", "Несуществующая книга"]
    for title in search_titles:
        try:
            author = hash_table[title]
            print_success(f"Книга '{title}' найдена, автор: {author}")
        except KeyError:
            print_error(f"Книга '{title}' не найдена в хеш-таблице")

    print_header("\n4. Содержимое хеш-таблицы:")
    hash_table.print_table()

    print_header("\n5. Удаление элементов:")
    delete_titles = ["Война и мир", "Идиот"]
    for title in delete_titles:
        try:
            del hash_table[title]
            print_success(f"Книга '{title}' успешно удалена")
        except KeyError:
            print_error(f"Ошибка при удалении: книга '{title}' не найдена")

    print_header("\n6. Информация о хеш-таблице после удаления:")
    print_info(str(hash_table))

    print_header("\n7. Полное содержимое хеш-таблицы:")
    hash_table.print_table()

    print_header("\n8. Анализ эффективности хеш-таблицы:")
    filled_buckets = sum(1 for tree in hash_table.table if tree is not BLANK)
    collision_buckets = sum(
        1 for tree in hash_table.table if tree is not BLANK and tree.collision
    )
    print_info(
        f"Заполнено ячеек: {filled_buckets} из {hash_table.capacity} ({filled_buckets/hash_table.capacity*100:.1f}%)"
    )
    print_info(
        f"Ячейки с коллизиями: {collision_buckets} ({collision_buckets/filled_buckets*100:.1f}% от заполненных)"
    )


if __name__ == "__main__":
    main()
