TRANSITIONS = [
    {0: 1, 1: 0},   # q0
    {0: 2, 1: 0},   # q1
    {0: 3, 1: 0},   # q2
    {0: 3, 1: 3},   # q3 (ловушка)
]
INITIAL_STATE = 0
FINAL_STATES = {0, 1, 2}
STATE_NAMES = ["q0", "q1", "q2", "q3"]


def recognize(chain):
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
    print("ДКА: запрещена подстрока '000'")
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
