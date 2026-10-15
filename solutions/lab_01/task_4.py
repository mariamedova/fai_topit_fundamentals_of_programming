student = "Анна Смирнова"
course = "Основы программирования на Python"
completed = 7
total = 10

print('1.', student[0], student[3])
print('2.', student[:4], student[5:])
print('3.', student.upper(), student.lower())
print('4.', student[0]+'.'+student[5]+'.')
print('5.', course[::-1])


score_percent = '70.0%'


str_percent_old = "%s — %s: %d/%d (%s)" % (student, course, completed, total, score_percent)
print("Оператор %:", str_percent_old)

# метод .format()
str_percent_format = "{} — {}: {}/{} ({})".format(student, course, completed, total, score_percent)
print("Метод .format():", str_percent_format)

# f‑строка
str_percent_f = f"{student} — {course}: {completed}/{total} ({score_percent})"
print("f-строка:", str_percent_f)

#------Unicode------

symbol = "Я"


print("символ:", symbol)
print("кодовая позиция (ord):", ord(symbol))
print("восстановление через chr():", chr(ord(symbol)))

encoded = symbol.encode("utf-8")
print("результат encode('utf-8'):", encoded)
print("длина байтовой последовательности:", len(encoded))

# Попытка изменить первый символ строки по индексу (это вызовет ошибку)
# symbol[0] = "А"