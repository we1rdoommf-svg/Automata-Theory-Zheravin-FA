import os

TRANSITIONS = {
    (0, 0): [0, 1], (0, 1): [0],
    (1, 0): [5, 2], (1, 1): [2],
    (2, 0): [3], (2, 1): [3],
    (3, 0): [4], (3, 1): [4],
    (4, 0): [1], (4, 1): [1],
    (5, 0): [5], (5, 1): [5],
}

INITIAL_STATE = 0
FINAL_STATES = {5}
STATE_NAMES = ["q0", "q1", "q2", "q3", "q4", "q5"]

INPUT_FILE = "test_strings_task_B.txt"


def recognize(chain):
    """
    Прогоняет цепочку по НКА.
    Возвращает (accepted: bool, path: list[str], error: str|None).
    Имитация всех копий НКА через множество текущих состояний.
    """
    current = {INITIAL_STATE}
    path = [STATE_NAMES[INITIAL_STATE]]

    for ch in chain:
        if ch == '0':
            symbol = 0
        elif ch == '1':
            symbol = 1
        else:
            return False, path, f"недопустимый символ '{ch}'"

        next_states = set()
        for state in current:
            if (state, symbol) in TRANSITIONS:
                for ns in TRANSITIONS[(state, symbol)]:
                    next_states.add(ns)

        if not next_states:
            return False, path, None

        current = next_states
        path.append("{" + ",".join(STATE_NAMES[s]
                    for s in sorted(current)) + "}")

    accepted = len(current & FINAL_STATES) > 0
    return accepted, path, None


def process_and_print(chain):
    """Прогоняет цепочку и печатает результат."""
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
            chain = ""
            for ch in line:
                if ch != '\n' and ch != '\r':
                    chain += ch
            if chain == "":
                continue
            process_and_print(chain)

    return True


def run_interactive():
    """Интерактивный режим: ввод цепочек с консоли."""
    print("=" * 60)
    print("НКА: два нуля, между которыми число символов кратно 4")
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
    if not run_from_file(INPUT_FILE):
        run_interactive()
    else:
        print("\n" + "=" * 60)
        print("Файл обработан. Переход в интерактивный режим.")
        print("Введите цепочку или 'exit' для выхода.")
        print("=" * 60)
        run_interactive()


if __name__ == "__main__":
    main()
