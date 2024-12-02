# Программа: "DFS method for puzzle"
# Программист: Морозов Д.С.
# Дата написания: 10.10.2024


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


def Appritiation(sit):
    """Функция, возвращающая ситуации по их оценке"""
    temp = []   # список сгенерированных ситуаций
    max_items = []  # список оценок для каждой ситуации
    for i in range(1, 5):
        next = NextSit(sit, i)  # генерируем новую ситуацию
        if next:
            temp.append(next)
            max_items.append(Grade(next))
    situations = [] # список ситуаций, отсортированных по их оцененному значеннию
    for i in range(len(max_items)):
        max_index = max_items.index(max(max_items)) # индекс ситуации с данной оценкой
        situations.append(temp[max_index])
        max_items.remove(max(max_items))
        temp.pop(max_index)
    return situations


def Grade(sit):
    situation = [sit[i][j] for i in range(len(sit)) for j in range(len(sit))]
    grade = 0
    # Просчет манхэтенского расстояния для каждой ячейки
    for i in range(len(situation)):
        if situation[i] != 0:
            grade += abs((i // 3 + 1) - ((situation[i] - 1) // 3 + 1)) + abs((i % 3)-((situation[i] - 1) % 3))
    # Возвращает оценку для ситуации
    return grade


def IsGoal(sit):
    """Функция проверки на достежение целевой ситуации"""
    return sit == goal_sit


def PrntSit(sit):
    """Процедура печати ситуации"""
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


def GradeSearch(sit, level=0):
    """Функция поиска в глубину"""
    if IsGoal(sit):  # проверка на достижение цели
        solution.append(sit)
        return True

    if level == level_limit:  # проверка на достижение ограничения
        return False

    for new_sit in Appritiation(sit):
        if new_sit and new_sit not in solution:  # Проверка на возможность ситуации при данном номере хода
            solution.append(sit)  # Добавляем текущую ситуацию в стек
            if GradeSearch(new_sit, level + 1):  # Рекурсивно вызываем DFS
                return True
            solution.pop()  # Убираем ситуацию, если не привела к решению

    return False


# начальная ситуация
start_sit = [[0, 2, 3],
             [1, 4, 5],
             [7, 8, 6]]

# целевая ситуация
goal_sit = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

solution = []  # Стек для хранения пути к решению
level_limit = int(input('Введите ограничение: '))


if not GradeSearch(start_sit):
    print(f"Решение не найдено при ограничении в {level_limit}")
else:
    print("Решение найдено!")
    n = 0
    for sit in solution:
        print(f'шаг {n}')
        PrntSit(sit)
        n += 1
