# ============================================================
# НКА: два нуля, между которыми число символов кратно 4
# Табличное представление автомата + консольный ввод
# ============================================================

# --- Состояния ---
# 0 = q0  — начальное, ищем первый ноль
# 1 = q1  — нашли первый ноль, отсчитываем 4 символа
# 2 = q2  — отсчитали 1 символ
# 3 = q3  — отсчитали 2 символа
# 4 = q4  — отсчитали 3 символа
# 5 = q5  — допускающее (нашли второй ноль на нужном расстоянии)

# --- Таблица переходов НКА: (state, symbol) -> list of next states ---
# symbol: 0 или 1
TRANSITIONS = {
    # q0: по 0 — остаться в q0 (ещё не первый ноль) ИЛИ перейти в q1 (угадали первый ноль)
    (0, 0): [0, 1],
    (0, 1): [0],

    # q1: по 0 — перейти в q5 (между нулями 0 символов) ИЛИ в q2 (начать отсчёт 4)
    (1, 0): [5, 2],
    (1, 1): [2],

    # q2: отсчитали 1 символ из 4
    (2, 0): [3],
    (2, 1): [3],

    # q3: отсчитали 2 символа
    (3, 0): [4],
    (3, 1): [4],

    # q4: отсчитали 3 символа
    (4, 0): [1],
    (4, 1): [1],

    # q5: допускающее, читаем всё подряд
    (5, 0): [5],
    (5, 1): [5],
}

# --- Начальное состояние ---
INITIAL_STATE = 0

# --- Допускающие состояния ---
FINAL_STATES = {5}

# --- Имена состояний (для вывода) ---
STATE_NAMES = ["q0", "q1", "q2", "q3", "q4", "q5"]


def recognize(chain):
    """
    Прогоняет цепочку по НКА.
    Возвращает (accepted: bool, path: list[str], error: str|None).
    Путь — один из успешных (если accepted) или кратчайший неуспешный.
    Без строковых функций — только посимвольный обход.
    """
    # Множество текущих состояний (имитация всех копий НКА)
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
            # Берём переходы из таблицы; если перехода нет — ветка умирает
            if (state, symbol) in TRANSITIONS:
                for ns in TRANSITIONS[(state, symbol)]:
                    next_states.add(ns)

        if not next_states:
            # Все ветки умерли — строка отвергается
            return False, path, None

        current = next_states
        path.append("{" + ",".join(STATE_NAMES[s]
                    for s in sorted(current)) + "}")

    accepted = len(current & FINAL_STATES) > 0
    return accepted, path, None


def print_result(chain, accepted, path, error):
    display = chain if chain != "" else "(пустая)"
    print(f"\nЦепочка: {display}")
    if error is not None:
        print(f"  Ошибка: {error}")
        print("  Результат: REJECTED")
        return
    print(f"  Путь: {' -> '.join(path)}")
    print(f"  Результат: {'ACCEPTED' if accepted else 'REJECTED'}")


def main():
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

        accepted, path, error = recognize(chain)
        print_result(chain, accepted, path, error)


if __name__ == "__main__":
    main()
