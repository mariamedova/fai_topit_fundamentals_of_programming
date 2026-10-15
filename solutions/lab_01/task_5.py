"""
Консольная программа для оформления карточки эксперимента.
Считывает данные исследователя, вычисляет временные показатели и
комплексный коэффициент, выводит результат в виде карточки.
"""


# --- Входные данные ---
name = input("Имя исследователя: ")
experiment = input("Название эксперимента: ")
runs = int(input("Количество выполненных запусков: "))
duration = float(input("Длительность одного запуска (с): "))
real = float(input("Действительная часть коэффициента: "))
imag = float(input("Мнимая часть коэффициента: "))

#---Вычисления---
total_seconds = runs * duration
total_minutes = total_seconds / 60
coefficient = complex(real, imag)
modulus_squared = real ** 2 + imag ** 2
has_runs = bool(runs)

#---Карточка результата---
print()
print("=" * 40)
print(f"ЭКСПЕРИМЕНТ: {experiment}")
print(f"Исследователь: {name}")
print(f"Запуски: {runs}")
print(f"Общее время: {total_seconds:.2f} с ({total_minutes:.2f} мин)")
print(f"Коэффициент: {coefficient}")
print(f"Квадрат модуля: {modulus_squared:.2f}")
print(f"Есть выполненные запуски: {has_runs}")
print("=" * 40)


"Диагностическая строка"
print(f"Типы: name={type(name).__name__}, experiment={type(experiment).__name__}, "
      f"runs={type(runs).__name__}, duration={type(duration).__name__}, "
      f"real={type(real).__name__}, imag={type(imag).__name__}")