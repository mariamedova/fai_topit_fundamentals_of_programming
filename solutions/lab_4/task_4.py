import re
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Submission:
    """Сдача лабораторной работы."""

    student_id: str
    laboratory_id: str
    attempt: int
    score: float
    comment: str = ""

    def __post_init__(self) -> None:
        # Вызывается автоматически после __init__ (dataclass).
        # Проверяет инварианты: непустые id, attempt > 0, score ∈ [0, 100].
        if not self.student_id:
            raise ValueError("student_id must be non-empty")
        if not self.laboratory_id:
            raise ValueError("laboratory_id must be non-empty")
        if self.attempt <= 0:
            raise ValueError("attempt must be positive")
        if not (0 <= self.score <= 100):
            raise ValueError("score must be in [0, 100]")


class Student:
    """Студент и его работы."""

    _ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

    def __init__(self, student_id: str, name: str) -> None:
        # Валидирует id (через is_valid_id) и имя, сохраняет их в приватные поля.
        # Список работ создаётся пустым.
        if not Student.is_valid_id(student_id):
            raise ValueError(f"invalid student_id: {student_id!r}")
        if not name:
            raise ValueError("name must be non-empty")
        self._id = student_id
        self._name = name
        self._submissions: list[Submission] = []

    @property
    def id(self) -> str:
        # Read-only доступ к приватному id.
        return self._id

    @property
    def name(self) -> str:
        # Read-only доступ к имени.
        return self._name

    @property
    def submissions(self) -> tuple[Submission, ...]:
        # Возвращает кортеж (копию) работ — снаружи нельзя изменить
        # внутренний список, только читать.
        return tuple(self._submissions)

    def add_submission(self, submission: Submission) -> None:
        # Добавляет работу, только если она принадлежит этому студенту.
        # Защищает инвариант «в списке нет чужих работ».
        if submission.student_id != self._id:
            raise ValueError(
                f"submission belongs to {submission.student_id!r}, "
                f"not to {self._id!r}"
            )
        self._submissions.append(submission)

    @property
    def average_score(self) -> float:
        # Средний балл по всем работам; 0.0, если работ нет.
        if not self._submissions:
            return 0.0
        return sum(s.score for s in self._submissions) / len(self._submissions)

    def best_score(self, laboratory_id: str) -> float | None:
        # Максимальный балл по конкретной лабе; None, если по ней нет работ.
        scores = [s.score for s in self._submissions
                  if s.laboratory_id == laboratory_id]
        return max(scores) if scores else None

    def sorted_submissions(self) -> list[Submission]:
        # Возвращает НОВЫЙ отсортированный список; исходный порядок
        # self._submissions не меняется.
        # Ключ: сначала лаба, потом попытка, потом балл.
        return sorted(self._submissions,
                      key=lambda s: (s.laboratory_id, s.attempt, s.score))

    def __len__(self) -> int:
        # Триггер len(student) — число попыток сдачи.
        return len(self._submissions)

    def __iter__(self) -> Iterator[Submission]:
        # Триггер for s in student: итерация по работам студента.
        # Возвращает итератор списка — новый при каждом вызове, поэтому
        # Student можно обходить многократно.
        return iter(self._submissions)

    def __str__(self) -> str:
        # Триггер str(student)/print: человекочитаемое представление.
        return f"Student({self._id}, {self._name}, attempts={len(self)})"

    def __repr__(self) -> str:
        # Триггер repr(student)/REPL/отладчик: однозначное представление
        # со всеми полями, по которому можно восстановить объект.
        return (f"Student(student_id={self._id!r}, name={self._name!r}, "
                f"submissions={self._submissions!r})")

    @classmethod
    def from_full_name(cls, student_id: str, full_name: str) -> "Student":
        # Альтернативный конструктор: создаёт Student из «Фамилия Имя».
        # Проверяет, что в full_name ≥ 2 слов.
        full_name = full_name.strip()
        if len(full_name.split()) < 2:
            raise ValueError("full_name must contain at least two words")
        return cls(student_id, full_name)

    @staticmethod
    def is_valid_id(student_id: str) -> bool:
        # Проверка формата id: начинается с буквы, дальше только
        # строчные буквы/цифры/подчёркивания.
        return bool(student_id) and bool(Student._ID_RE.match(student_id))


class Course:
    """Учебный курс."""

    def __init__(self, name: str = "Course") -> None:
        # Хранит имя и словарь студентов: id → Student.
        self._name = name
        self._students: dict[str, Student] = {}

    def add_student(self, student: Student) -> None:
        # Регистрирует студента; запрещает дубликат id.
        if student.id in self._students:
            raise ValueError(f"student {student.id!r} already registered")
        self._students[student.id] = student

    def get_student(self, student_id: str) -> Student:
        # Возвращает Student по id; KeyError, если не найден.
        return self._students[student_id]

    def submit(self, submission: Submission) -> None:
        # Принимает работу: находит студента по submission.student_id
        # и передаёт работу ему через add_submission.
        # KeyError, если студент не зарегистрирован.
        student = self._students.get(submission.student_id)
        if student is None:
            raise KeyError(f"unknown student: {submission.student_id!r}")
        student.add_submission(submission)

    def top_students(self, limit: int = 3) -> list[Student]:
        # Сортирует студентов по убыванию average_score и возвращает
        # первых limit. Возвращает новый список.
        return sorted(self._students.values(),
                      key=lambda s: s.average_score,
                      reverse=True)[:limit]

    def __contains__(self, student_id: object) -> bool:
        # Триггер `id in course`: проверка, зарегистрирован ли студент.
        return student_id in self._students

    def __len__(self) -> int:
        # Триггер len(course): число зарегистрированных студентов.
        return len(self._students)

    def __iter__(self) -> Iterator[Student]:
        # Триггер for s in course: итерация по значениям словаря.
        return iter(self._students.values())

    def __repr__(self) -> str:
        # Триггер repr(course): полное отладочное представление.
        return f"Course(name={self._name!r}, students={list(self._students)!r})"


if __name__ == "__main__":
    s1 = Student.from_full_name("ivanov", "Иван Иванов")
    s2 = Student("petrov", "Пётр Петров")
    s3 = Student("sidorova", "Анна Сидорова")
    print(s1, "|", repr(s1))
    print("is_valid_id('ivanov'):", Student.is_valid_id("ivanov"))
    print("is_valid_id('Ivanov'):", Student.is_valid_id("Ivanov"))

    course = Course("Python")
    for s in (s1, s2, s3):
        course.add_student(s)

    course.submit(Submission("ivanov", "lab1", 1, 70))
    course.submit(Submission("ivanov", "lab1", 2, 85, "исправлено"))
    course.submit(Submission("petrov", "lab1", 1, 90))
    course.submit(Submission("sidorova", "lab1", 1, 95))

    print("\n----- student -----")
    print("len(s1):", len(s1))
    print("avg s1:", s1.average_score)
    print("best s1 lab1:", s1.best_score("lab1"))
    print("submissions as tuple:", s1.submissions)

    print("\n----- course -----")
    print("len(course):", len(course))
    print("'ivanov' in course:", "ivanov" in course)
    print("'unknown' in course:", "unknown" in course)
    print("top-2:", [s.id for s in course.top_students(2)])

    print("\n----- sorted (не меняет исходный порядок) -----")
    print("original:", [(x.attempt, x.score) for x in s1])
    print("sorted:  ", [(x.attempt, x.score) for x in s1.sorted_submissions()])
    print("original after:", [(x.attempt, x.score) for x in s1])

    print("\n----- сравнение Submission по содержимому -----")
    a = Submission("ivanov", "lab2", 1, 80)
    b = Submission("ivanov", "lab2", 1, 80)
    print("a == b:", a == b)

    print("\n----- проверка инвариантов -----")
    for args in [
        ("", "lab1", 1, 50),
        ("ivanov", "lab1", 0, 50),
        ("ivanov", "lab1", 1, 150),
    ]:
        try:
            Submission(*args)
        except ValueError as e:
            print("  ValueError:", e)
