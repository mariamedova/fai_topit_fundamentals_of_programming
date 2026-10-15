import copy

original = [
    ["Python", 5],
    ["Algorithms", 4],
]

alias = original
shallow = original.copy()
deep = copy.deepcopy(original)

# Начальное состояние
print("-----Начальное состояние-----")
print("original:", original)
print("alias:", alias)
print("shallow:", shallow)
print("deep:", deep)
print("id(original):", id(original))
print("id(alias):", id(alias))
print("id(shallow):", id(shallow))
print("id(deep):", id(deep))
if original:
    print("id(original[0]):", id(original[0]))
    print("id(alias[0]):", id(alias[0]))
    print("id(shallow[0]):", id(shallow[0]))
    print("id(deep[0]):", id(deep[0]))
    if len(original[0]) > 1:
        print("id(original[0][1]):", id(original[0][1]))
        print("id(alias[0][1]):", id(alias[0][1]))
        print("id(shallow[0][1]):", id(shallow[0][1]))
        print("id(deep[0][1]):", id(deep[0][1]))

# Операция 1: original.append(["Databases", 5])
original.append(["Databases", 5])

print("\n-----После original.append([\"Databases\", 5])-----")
print("original:", original)
print("alias:", alias)
print("shallow:", shallow)
print("deep:", deep)
print()
print("id(original):", id(original))
print("id(alias):", id(alias))
print("id(shallow):", id(shallow))
print("id(deep):", id(deep))
print()
print("id(original[0]):", id(original[0]))
print("id(alias[0]):", id(alias[0]))
print("id(shallow[0]):", id(shallow[0]))
print("id(deep[0]):", id(deep[0]))
print()
print("id(original[0][1]):", id(original[0][1]))
print("id(alias[0][1]):", id(alias[0][1]))
print("id(shallow[0][1]):", id(shallow[0][1]))
print("id(deep[0][1]):", id(deep[0][1]))

# Операция 2: original[0][1] = 3
original[0][1] = 3

print()
print()
print("\n-----После original[0][1] = 3-----")
print("original:", original)
print("alias:", alias)
print("shallow:", shallow)
print("deep:", deep)
print()
print("id(original):", id(original))
print("id(alias):", id(alias))
print("id(shallow):", id(shallow))
print("id(deep):", id(deep))
print()
print("id(original[0]):", id(original[0]))
print("id(alias[0]):", id(alias[0]))
print("id(shallow[0]):", id(shallow[0]))
print("id(deep[0]):", id(deep[0]))
print()
print("id(original[0][1]):", id(original[0][1]))
print("id(alias[0][1]):", id(alias[0][1]))
print("id(shallow[0][1]):", id(shallow[0][1]))
print("id(deep[0][1]):", id(deep[0][1]))

print()
print()
print()

wrong_matrix = [[0] * 3] * 3
wrong_matrix[0][0] = 1

correct_matrix = [[0] * 3 for _ in range(3)]
correct_matrix[0][0] = 1

print("wrong_matrix:", wrong_matrix)
print("correct_matrix:", correct_matrix)

# Проверка идентичности вложенных строк
print("\nИдентичность строк в wrong_matrix:")
for i in range(3):
    print(f"id(wrong_matrix[{i}]):", id(wrong_matrix[i]))

print("\nИдентичность строк в correct_matrix:")
for i in range(3):
    print(f"id(correct_matrix[{i}]):", id(correct_matrix[i]))

