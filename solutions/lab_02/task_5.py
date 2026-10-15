import sys
import tracemalloc
'''
print("-----ЧАСТЬ 1: Размер отдельных объектов-----")

empty_list = []
list_10 = list(range(10))
tuple_10 = tuple(range(10))
str_10 = "x" * 10
int_obj = 42
none_obj = None

print(f"Размер пустого списка: {sys.getsizeof(empty_list)} байт")
print(f"Размер списка из 10 целых чисел: {sys.getsizeof(list_10)} байт")
print(f"Размер кортежа с 10 значениями: {sys.getsizeof(tuple_10)} байт")
print(f"Размер строки из 10 символов: {sys.getsizeof(str_10)} байт")
print(f"Размер целого числа: {sys.getsizeof(int_obj)} байт")
print(f"Размер объекта None: {sys.getsizeof(none_obj)} байт")
print()

print("-----ЧАСТЬ 2: Рост списка при append()-----")

lst = []
prev_size = sys.getsizeof(lst)

for i in range(100):
    lst.append(i)
    curr_size = sys.getsizeof(lst)
    if curr_size != prev_size:
        print(f"Длина: {len(lst)}, размер списка: {curr_size} байт, прирост: {curr_size - prev_size} байт")
        prev_size = curr_size

# Финальное состояние
print(f"Финальная длина: {len(lst)}, финальный размер списка: {sys.getsizeof(lst)} байт")
print()
'''

print("-----ЧАСТЬ 3: Сравнение range и list(range(...)) через tracemalloc-----")

# Сценарий с list(range(100_000))
tracemalloc.start()
obj_list = list(range(100_000))
current_list, peak_list = tracemalloc.get_traced_memory()
tracemalloc.stop()

size_list = sys.getsizeof(obj_list)
current_kb_list = current_list / 1024
peak_kb_list = peak_list / 1024

print("Сценарий: list_range_100k")
print(f"  Размер внешнего объекта: {size_list} байт")
print(f"  Текущая память: {current_kb_list:.2f} КБ")
print(f"  Пиковая память: {peak_kb_list:.2f} КБ")
print()

# Сценарий с range(100_000)
tracemalloc.start()
obj_range = range(100_000)
current_range, peak_range = tracemalloc.get_traced_memory()
tracemalloc.stop()

size_range = sys.getsizeof(obj_range)
current_kb_range = current_range / 1024
peak_kb_range = peak_range / 1024

print("Сценарий: range_100k")
print(f"  Размер внешнего объекта: {size_range} байт")
print(f"  Текущая память: {current_kb_range:.2f} КБ")
print(f"  Пиковая память: {peak_kb_range:.2f} КБ")
print()

# Отношение пиковых объёмов
if peak_kb_range > 0:
    ratio = peak_kb_list / peak_kb_range
else:
    ratio = float("inf")

print(f"Отношение пиковых объёмов (list/range): {ratio:.2f}")
print()