"""Задание 1. Протокол итерации."""

from typing import Any, Iterable, Iterator


def consume(iterable: Iterable) -> list:
    """Собирает элементы iterable, вручную используя iter() и next()."""
    lst = []
    it = iter(iterable)
    while True:
        try:
            lst.append(next(it))
        except StopIteration:
            break
    return lst


def my_enumerate(iterable: Iterable, start: int = 0) -> Iterator[tuple[int, Any]]:
    """Упрощённый аналог enumerate() без использования встроенного enumerate()."""
    count = start
    it = iter(iterable)
    while True:
        try:
            item = next(it)
        except StopIteration:
            return
        yield count, item
        count += 1


def my_zip(first: Iterable, second: Iterable) -> Iterator[tuple[Any, Any]]:
    """Упрощённый аналог zip(). Завершается по самому короткому источнику."""
    it1, it2 = iter(first), iter(second)
    while True:
        try:
            a = next(it1)
        except StopIteration:
            return
        try:
            b = next(it2)
        except StopIteration:
            return
        yield a, b


if __name__ == "__main__":
    print("----- Исследование протокола итерации -----")
    values = [10, 20, 30]
    iterator = iter(values)

    print("iterator is values:      ", iterator is values)          # False
    print("iter(iterator) is iterator:", iter(iterator) is iterator)  # True
    print(next(iterator))  # 10
    print(next(iterator))  # 20
    print(next(iterator))  # 30
    # print(next(iterator))  — StopIteration

    print("\n----- consume() -----")
    print(consume([1, 2, 3]))
    print(consume((1, 2, 3)))
    print(consume("abc"))
    print(consume(range(5)))

    partial = iter([1, 2, 3, 4])
    next(partial)                     # сдвинули на один элемент
    print("partial 1-й раз:", consume(partial))   # [2, 3, 4]
    print("partial 2-й раз:", consume(partial))   # [] (исчерпан)

    print("\n----- my_enumerate() -----")
    print(list(my_enumerate("abc")))
    print(list(my_enumerate([10, 20, 30], start=1)))

    print("\n----- my_zip() -----")
    print(list(my_zip([1, 2, 3], "abcd")))         # по короткому
    print(list(my_zip(range(10), "xy")))