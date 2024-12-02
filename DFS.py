"""
Решение игры "Пятнашки 3х3" методом просмотра в глубину.
"""

def FindZero(sit):
    """Функция для нахождения пустой ячейки (0)"""
    for i in range(3):
        for j in range(3):
            if sit[i][j] == 0:
                return i, j
    return None


def NextSit(sit, number):
    """Порождающая функция. Генерирует следующую ситуацию"""
    row, col = FindZero(sit)
    directions = {
        1: (row - 1, col),  # Вверх
        2: (row + 1, col),  # Вниз
        3: (row, col - 1),  # Влево
        4: (row, col + 1),  # Вправо
    }
    new_row, new_col = directions[number]
    if 0 <= new_row < 3 and 0 <= new_col < 3:   # проверка на возможность генерации ситуации с данным номером хода
        new_sit = [row[:] for row in sit]  # Копируем массив
        # Меняем местами пустую ячейку с целевой
        new_sit[row][col], new_sit[new_row][new_col] = new_sit[new_row][new_col], new_sit[row][col]
        return new_sit
    return False


def IsGoal(sit):
    """Функция проверки на достежение целевой ситуации"""
    return sit == goal_sit


def PrntSit(sit):
    """Процедура печати ситуации"""
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


def DFS(sit, level=0):
    """Функция поиска в глубину"""
    if IsGoal(sit):  # проверка на достижение цели
        solution.append(sit)
        return True

    if level == level_limit:  # проверка на достижение ограничения
        return False

    for number in range(1, 5):
        new_sit = NextSit(sit, number)
        if new_sit and new_sit not in solution:  # Проверка на возможность ситуации при данном номере хода
            solution.append(sit)  # Добавляем текущую ситуацию в стек
            if DFS(new_sit, level + 1):  # Рекурсивно вызываем DFS
                return True
            solution.pop()  # Убираем ситуацию, если не привела к решению

    return False


start_sit = [[2, 0, 3],
             [7, 4, 5],
             [8, 1, 6]]

goal_sit = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

solution = []  # Стек для хранения пути к решению
level_limit = int(input('Введите ограничение: '))


if not DFS(start_sit):
    print(f"Решение не найдено при ограничении в {level_limit}")
else:
    print("Решение найдено!")
    n = 0
    for sit in solution:
        print(f'шаг {n}')
        PrntSit(sit)
        n += 1
