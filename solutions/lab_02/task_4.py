import gc

first = []
second = []

first.append(second)
second.append(first)

print("first ссылается на second:", first[0] is second)
print("second ссылается на first:", second[0] is first)

# состояние сборщика мусора и статистика
print("\n--- Состояние сборщика мусора ---")
print("Автоматический сборщик мусора включён?", gc.isenabled())
print("Порог для поколений (0, 1, 2):", gc.get_threshold())
print("Статистика по поколениям:", gc.get_stats())

# запоминаем идентификаторы списков
id_first = id(first)
id_second = id(second)
print("\nID first:", id_first)
print("ID second:", id_second)

# удаляем имена first и second (сильные ссылки)
del first
del second

# запускаем сборку мусора
collected_count = gc.collect()
print("Количество собранных объектов после gc.collect():", collected_count)
print()
'''
'''print('----ДОПОЛНИТЕЛЬНЫЙ ЭКСПЕРИМЕНТ----')
print("Автосборщик включён?", gc.isenabled())
print("Пороги поколений:", gc.get_threshold())

# временно отключаем автоматический сборщик мусора
gc.disable()
print("\nАвтосборщик отключён. gc.isenabled() =", gc.isenabled())

# создаём несколько циклических структур
cycles = []
for i in range(3):
    a = []
    b = []
    a.append(b)
    b.append(a)
    cycles.append((a, b))

# для наглядности проверим, что циклы действительно есть
a0, b0 = cycles[0]
print("Проверка цикла 0: a0[0] is b0?", a0[0] is b0)
print("Проверка цикла 0: b0[0] is a0?", b0[0] is a0)

# удаляем внешние ссылки на циклы
del cycles
# Теперь на созданные пары (a, b) нет ни одной сильной ссылки извне, только взаимные ссылки внутри циклов
# запускаем сборку мусора вручную
collected = gc.collect()
print("\nПосле gc.collect(): собрано объектов:", collected)

# включаем автоматический сборщик обратно
gc.enable()
print("Автосборщик снова включён. gc.isenabled() =", gc.isenabled())

# финальная проверка
print("Финальные пороги:", gc.get_threshold())
print()
print()
print()

# Перед созданием графа получаем статистику сборщика мусора
before_stats = gc.get_count()  # (gen0, gen1, gen2) — количество объектов в каждом поколении
print(f"Статистика до создания графа: {before_stats}")

# создание модели графа
node_a = {"name": "A", "neighbors": []} # узел 1
node_b = {"name": "B", "neighbors": []} # узел 2
node_c = {"name": "C", "neighbors": []} # узел 3
node_d = {"name": "D", "neighbors": []} # узел 4

# цикл: A -> B -> C -> A
node_a["neighbors"].append(node_b)
node_b["neighbors"].append(node_c)
node_c["neighbors"].append(node_a)

print("\nСвязи в графе:")
print(f"A -> B (id B: {id(node_b)})")
print(f"B -> C (id C: {id(node_c)})")
print(f"C -> A (id A: {id(node_a)})")
print(f"D (независимый): id = {id(node_d)}")

# сохраняем идентификаторы циклических узлов, чтобы потом проверить, что они исчезли
ids_cycle = {id(node_a), id(node_b), id(node_c)}
id_independent = id(node_d)

del node_a, node_b, node_c # удаляем внешние имена, ссылающиеся на циклические узлы
# node_d остаётся доступным по имени

print(f"\nПосле удаления имен node_a/b/c: node_d всё ещё доступен? {node_d is not None}")
print(f"ID независимого узла D: {id_independent}")

# запускаем ручную сборку мусора
collected_count = gc.collect()
print(f"Количество собранных объектов при ручной сборке: {collected_count}")

# после сборки проверяем, что циклические узлы действительно удалены
# попытаемся найти их по ID — но у нас нет прямых ссылок, поэтому смотрим статистику
after_stats = gc.get_count()
print(f"Статистика после сборки: {after_stats}")

# Дополнительная проверка: независимый узел должен быть доступен
print(f"Независимый узел D доступен: name = {node_d['name']}, neighbors = {node_d['neighbors']}")
print()
