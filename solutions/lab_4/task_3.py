from collections import deque
from typing import Iterable, Iterator


def read_measurements(lines: Iterable[str]) -> Iterator[float]:
    """Преобразует непустые строки в вещественные числа."""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        yield float(line)


def filter_range(values: Iterable[float],
                 minimum: float, maximum: float) -> Iterator[float]:
    """Пропускает значения из закрытого диапазона [minimum, maximum]."""
    for v in values:
        if minimum <= v <= maximum:
            yield v


def moving_average(values: Iterable[float], window_size: int) -> Iterator[float]:
    """Выдаёт скользящее среднее; хранит только window_size последних значений."""
    if window_size <= 0:
        raise ValueError("window_size must be positive")
    window: deque[float] = deque(maxlen=window_size)
    for v in values:
        window.append(v)
        if len(window) == window_size:
            yield sum(window) / window_size


def take(n: int, iterable: Iterable) -> Iterator:
    """Первые n элементов iterable."""
    if n < 0:
        raise ValueError("n must be non-negative")
    it = iter(iterable)
    for _ in range(n):
        try:
            yield next(it)
        except StopIteration:
            return


def drop(n: int, iterable: Iterable) -> Iterator:
    """Пропускает первые n элементов, отдаёт остальные."""
    it = iter(iterable)
    for _ in range(n):
        try:
            next(it)
        except StopIteration:
            return
    yield from it


def batch(iterable: Iterable, size: int) -> Iterator[list]:
    """Разбивает iterable на пачки по size элементов (без материализации)."""
    if size <= 0:
        raise ValueError("size must be positive")
    buf: list = []
    for item in iterable:
        buf.append(item)
        if len(buf) == size:
            yield buf
            buf = []
    if buf:
        yield buf


if __name__ == "__main__":
    raw_lines = ["10.0", "", "12.5", "100.0", "11.5", "13.0", "9.5"]

    print("----- Конвейер -----")
    pipeline = moving_average(
        filter_range(read_measurements(raw_lines), 9.0, 15.0),
        window_size=2,
    )
    print(next(pipeline))   # 11.25
    print(next(pipeline))   # 12.0
    print(list(pipeline))   # [12.25, 12.25, 11.25]
    print(list(pipeline))   # [] — исчерпан

    print("\n----- Новый конвейер -----")
    pipeline2 = moving_average(
        filter_range(read_measurements(raw_lines), 9.0, 15.0), 2
    )
    print(list(pipeline2))

    print("\n----- take / drop / batch -----")
    src = read_measurements(raw_lines)
    processed = filter_range(src, 9.0, 15.0)
    first = list(take(3, drop(1, processed)))
    print("take(3, drop(1, ...)):", first)

    full = filter_range(read_measurements(raw_lines), 0, 100)
    print("batch(size=3):", list(batch(full, 3)))

    print("\n----- Включения vs генераторные выражения -----")
    squares = [x * x for x in range(1, 21) if x % 2 == 0]
    print("squares (list comp):", squares)

    lengths = {len(s) for s in ["a", "", "abc", "hello"] if s}
    print("lengths (set comp):", lengths)

    squares_dict = {x: x * x for x in range(1, 11)}
    print("squares_dict:", squares_dict)

    total = sum(x * x for x in range(1_000_000))
    print("sum of squares 1e6 (generator):", total)

    print("\n----- tracemalloc: lazy vs lists -----")
    import tracemalloc

    N = 100_000

    tracemalloc.start()
    lazy_total = sum(moving_average(
        filter_range((float(i) for i in range(N)), 0, N),
        window_size=10,
    ))
    _, lazy_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    numbers = [float(i) for i in range(N)]
    filtered = [x for x in numbers if 0 <= x <= N]
    avgs = list(moving_average(filtered, 10))
    list_total = sum(avgs)
    _, list_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"lazy peak: {lazy_peak / 1024:.1f} KiB  (sum={lazy_total:.1f})")
    print(f"list peak: {list_peak / 1024 / 1024:.2f} MiB (sum={list_total:.1f})")