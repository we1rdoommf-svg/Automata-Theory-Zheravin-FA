# ============================================================
# ДКА: строка не начинается с "01" и не содержит "000"
# Табличное представление автомата
# Режимы: чтение из файла или консольный ввод
# ============================================================

import os

# --- Таблица переходов ---
TRANSITIONS = [
    {0: 2, 1: 1},   # q0 — начало строки
    {0: 4, 1: 1},   # q1 — первый символ "1"
    {0: 3, 1: 6},   # q2 — первый символ "0"
    {0: 6, 1: 1},   # q3 — начало "00"
    {0: 5, 1: 1},   # q4 — один "0" в конце
    {0: 6, 1: 1},   # q5 — два "0" в конце
    {0: 6, 1: 6},   # q6 — ловушка
]

INITIAL_STATE = 0
FINAL_STATES = {1, 2, 3, 4, 5}
STATE_NAMES = ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]

INPUT_FILE = "test_strings_task_A.txt"


def recognize(chain):
    """
    Прогоняет цепочку по ДКА.
    Возвращает (accepted: bool, path: list[str], error: str|None).
    Без строковых функций — только посимвольный обход.
    """
    state = INITIAL_STATE
    path = [STATE_NAMES[state]]

    for ch in chain:
        if ch == '0':
            symbol = 0
        elif ch == '1':
            symbol = 1
        else:
            return False, path, f"недопустимый символ '{ch}'"

        state = TRANSITIONS[state][symbol]
        path.append(STATE_NAMES[state])

    accepted = state in FINAL_STATES
    return accepted, path, None


def process_and_print(chain):
    """Прогоняет цепочку и печатает результат в формате, похожем на JFLAP."""
    accepted, path, error = recognize(chain)
    display = chain if chain != "" else "(пустая)"
    print(f"\nЦепочка: {display}")
    if error is not None:
        print(f"  Ошибка: {error}")
        print("  Результат: REJECTED")
    else:
        print(f"  Путь: {' -> '.join(path)}")
        print(f"  Результат: {'ACCEPTED' if accepted else 'REJECTED'}")


def run_from_file(filename):
    """Считывает цепочки из файла (по одной на строку) и прогоняет каждую."""
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден. Переход в интерактивный режим.")
        return False

    print("=" * 60)
    print(f"Чтение цепочек из файла: {filename}")
    print("=" * 60)

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # Убираем символы перевода строки вручную, без строковых методов
            chain = ""
            for ch in line:
                if ch != '\n' and ch != '\r':
                    chain += ch
            # Пропускаем пустые строки-разделители (но не пустую цепочку)
            if chain == "":
                continue
            process_and_print(chain)

    return True


def run_interactive():
    """Интерактивный режим: ввод цепочек с консоли."""
    print("=" * 60)
    print("ДКА: нет '000' и нет начала '01'")
    print("Алфавит: {0, 1}")
    print("Введите цепочку или 'exit' для выхода.")
    print("=" * 60)

    while True:
        try:
            chain = input("\n> ").strip()
        except EOFError:
            break

        if chain == "exit":
            print("Выход.")
            break

        process_and_print(chain)


def main():
    # Сначала пробуем файл
    if not run_from_file(INPUT_FILE):
        # Если файла нет — работаем в интерактивном режиме
        run_interactive()
    else:
        # После файла можно продолжить вручную
        print("\n" + "=" * 60)
        print("Файл обработан. Переход в интерактивный режим.")
        print("Введите цепочку или 'exit' для выхода.")
        print("=" * 60)
        run_interactive()


if __name__ == "__main__":
    main()
