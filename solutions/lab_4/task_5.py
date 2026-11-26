from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Callable, Iterator


# ---------- Иерархия событий ----------

class CourseEvent(ABC):
    """Базовое событие журнала."""

    def __init__(self, student_id: str,
                 created_at: datetime | None = None) -> None:
        # Общая инициализация всех событий: id студента и время создания
        # (если не передано — текущий момент).
        if not student_id:
            raise ValueError("student_id must be non-empty")
        self._student_id = student_id
        self._created_at = created_at or datetime.now()

    @property
    def student_id(self) -> str:
        # Read-only id студента, к которому относится событие.
        return self._student_id

    @property
    def created_at(self) -> datetime:
        # Read-only время создания события.
        return self._created_at

    @abstractmethod
    def describe(self) -> str:
        # Абстрактный контракт: каждый наследник обязан вернуть строку.
        # Обеспечивает полиморфизм для render_timeline().
        ...

    def __repr__(self) -> str:
        # Общее отладочное представление для всех событий.
        return (f"{type(self).__name__}(student_id={self._student_id!r}, "
                f"created_at={self._created_at!r})")


class SubmissionEvent(CourseEvent):
    def __init__(self, student_id: str, laboratory_id: str,
                 attempt: int, score: float,
                 created_at: datetime | None = None) -> None:
        # Инициализация «общей части» через super().__init__,
        # затем валидация и сохранение специфичных полей события сдачи.
        super().__init__(student_id, created_at)
        if attempt <= 0:
            raise ValueError("attempt must be positive")
        if not (0 <= score <= 100):
            raise ValueError("score must be in [0, 100]")
        self._laboratory_id = laboratory_id
        self._attempt = attempt
        self._score = score

    @property
    def laboratory_id(self) -> str:
        # Read-only id лабораторной.
        return self._laboratory_id

    @property
    def attempt(self) -> int:
        # Read-only номер попытки.
        return self._attempt

    @property
    def score(self) -> float:
        # Read-only балл.
        return self._score

    def describe(self) -> str:
        # Человекочитаемое описание для временной шкалы.
        return (f"{self._created_at:%Y-%m-%d %H:%M} — сдача лаб."
                f"{self._laboratory_id}, попытка {self._attempt}, "
                f"{self._score} баллов")


class AttendanceEvent(CourseEvent):
    def __init__(self, student_id: str, lesson: str, present: bool,
                 created_at: datetime | None = None) -> None:
        # Сохраняет название занятия и факт присутствия.
        super().__init__(student_id, created_at)
        self._lesson = lesson
        self._present = present

    def describe(self) -> str:
        # Формирует строку «присутствовал/отсутствовал на занятии ...».
        status = "присутствовал(а)" if self._present else "отсутствовал(а)"
        return (f"{self._created_at:%Y-%m-%d %H:%M} — {status} "
                f"на занятии «{self._lesson}»")


class CommentEvent(CourseEvent):
    def __init__(self, student_id: str, text: str,
                 created_at: datetime | None = None) -> None:
        # Валидирует непустой текст и сохраняет его.
        super().__init__(student_id, created_at)
        if not text:
            raise ValueError("text must be non-empty")
        self._text = text

    def describe(self) -> str:
        # Формирует строку с текстом комментария.
        return f"{self._created_at:%Y-%m-%d %H:%M} — комментарий: «{self._text}»"


# Практическое расширение: новый тип, добавленный БЕЗ изменения render_timeline

class DeadlineEvent(CourseEvent):
    def __init__(self, student_id: str, laboratory_id: str, deadline: datetime,
                 created_at: datetime | None = None) -> None:
        # Новый тип события: дедлайн по лабораторной.
        super().__init__(student_id, created_at)
        self._laboratory_id = laboratory_id
        self._deadline = deadline

    def describe(self) -> str:
        # Реализация того же интерфейса, что и у остальных событий —
        # поэтому render_timeline продолжает работать без правок.
        return (f"{self._created_at:%Y-%m-%d %H:%M} — напоминание о дедлайне "
                f"по лаб.{self._laboratory_id}: {self._deadline:%Y-%m-%d}")


# ---------- Журнал ----------

class CourseJournal:
    """Журнал событий курса."""

    def __init__(self) -> None:
        # Внутреннее хранилище событий в порядке добавления.
        self._events: list[CourseEvent] = []

    def add(self, event: CourseEvent) -> None:
        # Добавляет событие в конец журнала.
        self._events.append(event)

    def __len__(self) -> int:
        # Триггер len(journal): общее число событий.
        return len(self._events)

    def __iter__(self) -> Iterator[CourseEvent]:
        # Триггер for e in journal: итерация по событиям в порядке добавления.
        return iter(self._events)

    def __getitem__(self, key):
        # Триггер journal[i] и journal[a:b]: доступ по индексу и срезу.
        # Срез возвращает новый список (копию), индекс — сам элемент.
        return self._events[key]

    def __str__(self) -> str:
        # Триггер str(journal)/print: краткая сводка.
        return f"CourseJournal({len(self._events)} events)"

    def __repr__(self) -> str:
        # Триггер repr(journal)/REPL/отладчик: полное представление.
        return f"CourseJournal(events={self._events!r})"

    def events_for_student(self, student_id: str) -> Iterator[CourseEvent]:
        # Генератор: лениво фильтрует события по id студента.
        # Не создаёт промежуточный список — работает по одному событию.
        for e in self._events:
            if e.student_id == student_id:
                yield e

    def events_by_type(self, event_type: type) -> Iterator[CourseEvent]:
        # Генератор: лениво фильтрует события по классу.
        for e in self._events:
            if isinstance(e, event_type):
                yield e

    def summary(self) -> dict[str, Any]:
        # Возвращает НОВЫЙ dict с агрегатами:
        # total, by_type, average_score, students.
        # Внутренний список событий не раскрывается.
        by_type: dict[str, int] = {}
        for e in self._events:
            by_type[type(e).__name__] = by_type.get(type(e).__name__, 0) + 1
        scores = [e.score for e in self._events if isinstance(e, SubmissionEvent)]
        return {
            "total": len(self._events),
            "by_type": dict(by_type),
            "average_score": (sum(scores) / len(scores)) if scores else None,
            "students": len({e.student_id for e in self._events}),
        }


# ---------- Полиморфный рендер ----------

def render_timeline(events) -> str:
    # Формирует временную шкалу, вызывая describe() у каждого события.
    # Не проверяет isinstance — работает за счёт полиморфизма, поэтому
    # добавление нового типа события не требует правок здесь.
    return "\n".join(f"  • {e.describe()}" for e in events)


# ---------- Пользовательские представления ----------

class ScoreView:
    """Лениво обходит только результаты сдач. Повторно обходим."""

    def __init__(self, journal: CourseJournal) -> None:
        # Сохраняет ссылку на журнал; сам список событий не копирует.
        self._journal = journal

    def __iter__(self) -> Iterator[float]:
        # Каждый вызов iter(view) создаёт новый генератор,
        # поэтому представление можно обходить многократно.
        # Отдаёт только score у SubmissionEvent.
        for e in self._journal:
            if isinstance(e, SubmissionEvent):
                yield e.score


class FilteredJournalView:
    """Ленивое представление журнала с предикатом."""

    def __init__(self, journal: CourseJournal,
                 predicate: Callable[[CourseEvent], bool]) -> None:
        # Сохраняет журнал и предикат; фильтрация произойдёт при обходе.
        self._journal = journal
        self._predicate = predicate

    def __iter__(self) -> Iterator[CourseEvent]:
        # Генератор: отдаёт события, для которых предикат вернул True.
        # Повторный обход даёт тот же результат (генератор создаётся заново).
        for e in self._journal:
            if self._predicate(e):
                yield e

    def __len__(self) -> int:
        # Число подходящих событий; считается обходом (O(n)),
        # но внутренний список не раскрывается.
        return sum(1 for _ in self)


# ---------- Демонстрация ----------

if __name__ == "__main__":
    now = datetime(2025, 1, 15, 9, 0)
    journal = CourseJournal()

    events = [
        AttendanceEvent("ivanov",   "Python #1", True,  now + timedelta(hours=1)),
        SubmissionEvent("ivanov",   "lab1", 1, 70,       now + timedelta(hours=2)),
        CommentEvent   ("ivanov",   "исправь отчёт",     now + timedelta(hours=3)),
        SubmissionEvent("ivanov",   "lab1", 2, 85,       now + timedelta(days=1)),
        AttendanceEvent("petrov",   "Python #1", True,   now + timedelta(hours=1)),
        SubmissionEvent("petrov",   "lab1", 1, 92,       now + timedelta(days=1)),
        CommentEvent   ("petrov",   "отлично",           now + timedelta(days=1, hours=1)),
        AttendanceEvent("sidorova", "Python #1", False,  now + timedelta(hours=1)),
        SubmissionEvent("sidorova", "lab1", 1, 95,       now + timedelta(days=2)),
        DeadlineEvent  ("sidorova", "lab2",              now + timedelta(days=7),
                        now + timedelta(days=1)),
    ]
    for e in events:
        journal.add(e)

    print("----- len / repr / str -----")
    print(len(journal))
    print(str(journal))
    print(repr(journal)[:80], "...")

    print("\n----- Индексация и срез -----")
    print("journal[0]:", journal[0].describe())
    print("срез [2:5]:")
    for e in journal[2:5]:
        print("  ", e.describe())

    print("\n----- events_for_student('ivanov') -----")
    for e in journal.events_for_student("ivanov"):
        print("  ", e.describe())

    print("\n----- events_by_type(AttendanceEvent) -----")
    for e in journal.events_by_type(AttendanceEvent):
        print("  ", e.describe())

    print("\n----- render_timeline (полиморфно) -----")
    print(render_timeline(journal))

    print("\n----- ScoreView: средний балл по сдачам -----")
    scores = list(ScoreView(journal))
    print("scores:", scores)
    print("avg   :", sum(scores) / len(scores))

    print("\n----- summary() -----")
    print(journal.summary())

    print("\n----- FilteredJournalView -----")

    def is_submission(e: CourseEvent) -> bool:
        # Именованная функция-предикат: пропускает только события сдачи.
        return isinstance(e, SubmissionEvent)

    v1 = FilteredJournalView(journal, is_submission)
    v2 = FilteredJournalView(journal, lambda e: e.student_id == "ivanov")
    print("only submissions:", [e.describe() for e in v1])
    print("only ivanov     :", [e.describe() for e in v2])
    print("повторный обход v2:", len(list(v2)), "==", len(list(v2)))