"""Задание 2. Собственный итератор StepRange."""

from typing import Iterator


class StepRange:
  # Итерируемая последовательность целых с произвольным ненулевым шагом.

    __slots__ = ("_start", "_stop", "_step")

    def __init__(self, start: int, stop: int, step: int = 1) -> None:
        if step == 0:
            raise ValueError("шаг не может быть нулевым")
        self._start = int(start)
        self._stop = int(stop)
        self._step = int(step)

    def __iter__(self) -> "StepRangeIterator":
        return StepRangeIterator(self._start, self._stop, self._step)

    def __len__(self) -> int:
        if self._step > 0:
            if self._start >= self._stop:
                return 0
            return (self._stop - self._start - 1) // self._step + 1
        else:
            if self._start <= self._stop:
                return 0
            return (self._start - self._stop - 1) // (-self._step) + 1

    def __contains__(self, value: object) -> bool:
        if not isinstance(value, int):
            return False
        if self._step > 0:
            if not (self._start <= value < self._stop):
                return False
        else:
            if not (self._stop < value <= self._start):
                return False
        return (value - self._start) % self._step == 0

    def __repr__(self) -> str:
        return f"StepRange({self._start}, {self._stop}, {self._step})"


class StepRangeIterator:
    """Итератор StepRange. Хранит собственное состояние обхода."""

    __slots__ = ("_current", "_stop", "_step")

    def __init__(self, start: int, stop: int, step: int) -> None:
        self._current = start
        self._stop = stop
        self._step = step

    def __iter__(self) -> "StepRangeIterator":
        return self

    def __next__(self) -> int:
        if self._step > 0:
            if self._current >= self._stop:
                raise StopIteration
        else:
            if self._current <= self._stop:
                raise StopIteration
        value = self._current
        self._current += self._step
        return value


if __name__ == "__main__":
    print("----- Граничные случаи -----")
    print(list(StepRange(0, 5, 1)))    # [0,1,2,3,4]
    print(list(StepRange(5, 0, -1)))   # [5,4,3,2,1]
    print(list(StepRange(0, 0, 1)))    # []
    print(list(StepRange(0, 5, -1)))   # []
    print(list(StepRange(2, 11, 3)))   # [2,5,8]

    print("\n----- Два независимых итератора -----")
    sr = StepRange(2, 11, 3)
    it1, it2 = iter(sr), iter(sr)
    print(next(it1))  # 2
    print(next(it2))  # 2
    print(next(it1))  # 5
    print(next(it2))  # 5
    print(next(it1))  # 8
    print(next(it2))  # 8
    # next(it1)  # StopIteration

    print("\n----- len / in / repr -----")
    print(len(StepRange(0, 10, 2)))         # 5
    print(len(StepRange(10, 0, -2)))        # 5
    print(8 in StepRange(0, 10, 2))         # True
    print(7 in StepRange(0, 10, 2))         # False
    print(repr(StepRange(2, 11, 3)))        # StepRange(2, 11, 3)

    print("\n----- my_enumerate / my_zip из task_1 на StepRange -----")
    from task_1 import my_enumerate, my_zip
    print(list(my_enumerate(StepRange(2, 11, 3))))
    print(list(my_zip(StepRange(2, 11, 3), "abc")))

    print("\n----- Сравнение: __contains__ vs полный перебор -----")

def count_iterations(step_range, target):
    """Явный перебор с подсчётом числа итераций."""
    n = 0
    for v in step_range:
        n += 1
        if v == target:
            return n, True
    return n, False

# Возьмём диапазон, где target ЕСТЬ, чтобы исходы совпали
sr = StepRange(0, 10**6, 1)
target = 999_999

# 1) через __contains__ — O(1), ни одной итерации
contains_result = target in sr

# 2) через явный перебор — сколько итераций потребовалось
iters, found = count_iterations(sr, target)

print(f"__contains__: результат={contains_result}, "
      f"итераций=0, арифметических операций=O(1)")
print(f"перебор:      результат={found}, итераций={iters}, O(n)")

'''Для диапазона 10**9 полный перебор занял бы ~10^9 итераций
(не запускаем — это минуты), т.е. в ~1000 раз больше операций,
чем для 10**6, при том что __contains__ остаётся O(1).'''