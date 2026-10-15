import sys

data = [1, 2, 3]
print("После создания:", sys.getrefcount(data)) #прогноз - 1, но получаем 2

alias = data
print("После создания alias:", sys.getrefcount(data)) #прогноз - 2, но получаем 3

container = [data]
print("После помещения в контейнер:", sys.getrefcount(data)) #прогноз - 3, но получаем 4

del alias
print("После del alias:", sys.getrefcount(data)) #прогноз - 2, но получаем 3

container.clear()
print("После очистки контейнера:", sys.getrefcount(data)) #прогноз - 1, но получаем 2




import weakref


class Record:
    pass


record = Record()
weak_record = weakref.ref(record)

print(weak_record())
del record
print(weak_record())


import weakref

class Record:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Record({self.name!r})"

# Создаём реестр со слабыми ссылками на значения
registry = weakref.WeakValueDictionary()

r1 = Record("A")
r2 = Record("B")
r3 = Record("C")

# Добавляем все три в реестр
registry["A"] = r1
registry["B"] = r2
registry["C"] = r3

print("Реестр сразу после добавления:", dict(registry))

# Оставляем сильные ссылки только на r1 и r2, а для r3 убираем сильную ссылку
temp_r3 = r3 # временная сильная ссылка
del r3 # убираем основную сильную ссылку на r3
print("\nПосле удаления r3 (но temp_r3 ещё есть):", dict(registry))

del temp_r3 # убираем последнюю сильную ссылку на объект C
print("После удаления temp_r3:", dict(registry))

del r2 # Удаляем ещё одну сильную ссылку — r2
print("После удаления r2:", dict(registry))

print("Итоговый реестр:", dict(registry))
print()
