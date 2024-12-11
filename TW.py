"""
Решение игры "Пятнашки 3х3" методом двунаправленного поиска.
"""


# Класс, представляющий собой вершину дерева решений
class Sit:
    def __init__(self, sit, prev):
        self.value = sit    # Хранит ситуацию
        self.previous = prev    # Хранит предыдущую вершину


# Функция для нахождения пустой ячейки (0)
# Входные данные: Ситуация
def FindZero(sit):
    for i in range(3):
        for j in range(3):
            if sit[i][j] == 0:
                return i, j
    return None


# Порождающая функция. Генерирует следующую ситуацию
# Входные данные: Ситуация, номер следующего хода
def NextSit(sit, number):
    row, col = FindZero(sit)
    directions = {
        1: (row - 1, col),  # Вверх
        2: (row + 1, col),  # Вниз
        3: (row, col - 1),  # Влево
        4: (row, col + 1),  # Вправо
    }
    new_row, new_col = directions[number]
    if 0 <= new_row < 3 and 0 <= new_col < 3:  # проверка на возможность генерации ситуации с данным номером хода
        new_sit = [row[:] for row in sit]  # Копируем массив
        # Меняем местами пустую ячейку с целевой
        new_sit[row][col], new_sit[new_row][new_col] = new_sit[new_row][new_col], new_sit[row][col]
        return new_sit
    return False


# Процедура печати ситуации
# Входные данные: Ситуация
def PrntSit(sit):
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


# Функция, реализующая метод двунаправленного поиска
# Входные данные: Начальная и Целевая ситуации
def TwoSidedSearch(situation, goal_situation):
    start_sit = Sit(situation, None)  # Создается объект класса Sit - корень дерева
    goal_sit = Sit(goal_situation, None)    # Создается объект класса Sit - корень дерева

    level_start = [start_sit]   # Список, хранящий вершины текущего уровня, для поиска с начальной вершины
    level_goal = [goal_sit]   # Список, хранящий вершины текущего уровня, для поиска с целевой вершины

    visited_start = [situation]  # Список для хранения посещенных вершин для поиска с начальной вершины
    visited_goal = [goal_situation]  # Список для хранения посещенных вершин для поиска с целевой вершины
    while True:  # Поиск в ширину через цикл

        temp = []
        for sit in level_start:
            for number in range(1, 5):
                new_sit = NextSit(sit.value, number)  # Генерируем возможные ситуации
                if new_sit and new_sit not in visited_start:  # Проверка, что ситуация еще не была посещена
                    visited_start.append(new_sit)
                    temp.append(Sit(new_sit, sit))  # Добавляем в список
        level_start = temp
        for sit_s in level_start:
            for sit_g in level_goal:
                if sit_s.value == sit_g.value:
                    solution = []
                    while sit_s != None:
                        solution.append(sit_s.value)
                        sit_s = sit_s.previous
                    solution.reverse()
                    solution.pop()
                    while sit_g != None:
                        solution.append(sit_g.value)
                        sit_g = sit_g.previous
                    return solution
        temp = []
        for sit in level_goal:
            for number in range(1, 5):
                new_sit = NextSit(sit.value, number)  # Генерируем возможные ситуации
                if new_sit and new_sit not in visited_goal:  # Проверка, что ситуация еще не была посещена
                    visited_goal.append(new_sit)
                    temp.append(Sit(new_sit, sit))  # Добавляем в список
        level_goal = temp
        for sit_s in level_start:
            for sit_g in level_goal:
                if sit_s.value == sit_g.value:
                    solution = []
                    while sit_s != None:
                        solution.append(sit_s.value)
                        sit_s = sit_s.previous
                    solution.reverse()
                    solution.pop()
                    while sit_g != None:
                        solution.append(sit_g.value)
                        sit_g = sit_g.previous
                    return solution


# начальная ситуация
start_sit = [[2, 0, 3],
             [7, 4, 5],
             [8, 1, 6]]

# целевая ситуация
goal_sit = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

solution = TwoSidedSearch(start_sit, goal_sit)  # Список для хранения пути к решению


if solution is None:
    print("Решение не найдено")
else:
    print("Решение найдено!")
    for n, sit in enumerate(solution):
        print(f'Шаг {n}')
        PrntSit(sit)
