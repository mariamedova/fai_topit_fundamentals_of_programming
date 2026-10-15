#-----A-----
print('-----Экспенимент A-----')

a = 10
b = a

print(a, b)
print(id(a), id(b))

a += 1

print(a, b)
print(id(a), id(b))
print()

# -----B-----
print('-----Экспенимент B-----')

first = [10, 20]
second = first

print(first, second)
print(id(first), id(second))

second.append(30)

print(first, second)
print(id(first), id(second))

second = [10, 20, 30]

print(first == second)
print(first is second)

second.append(40)

print(first)
print()

print('-----Практическая задача-----')

import copy

config1 = {'название': 'А муха тоже вертолет',
           'список участников': ['Буслова С.А.', 'Попов А.С.', 'Гоголь Н.В', 'Мишель де Нотрдам', 'Артём', 'Nordax S.S.'],
           'параметры запуска': [17, 239.0, 88005553535, 56.8, 69.96]}

#вторая конфигурация с нежелательным совместным изменением
config2 = config1
config2['название'] = 'Бытие мое'
print('До изменений:')
print('config1 == config2:', config1 == config2)
print(config1)
print(config2)

config2 = copy.deepcopy(config1)
config2['название'] = 'Небытие мое'
config2['параметры запуска'].append(9.11)
print()

#вторая конфигурация без нежелательных совместных изменений
print('После изменений:')
print('config1 == config2:', config1 == config2)
print(config1)
print(config2)


