from collections import deque


class Node:
    def __init__(self, sit, prev):
        self.value = sit
        self.previous = prev


def FindZero(sit):
    """Функция для нахождения пустой ячейки (0)"""
    for i in range(3):
        for j in range(3):
            if sit[i][j] == 0:
                return i, j
    return None


def NextSit(sit):
    """Порождающая функция. Генерирует следующую ситуацию"""
    row, col = FindZero(sit)
    directions = {
        1: (row - 1, col),  # Вверх
        2: (row + 1, col),  # Вниз
        3: (row, col - 1),  # Влево
        4: (row, col + 1),  # Вправо
    }
    sits = []
    for i in range(1, 5):
        new_row, new_col = directions[i]
        if 0 <= new_row < 3 and 0 <= new_col < 3:   # проверка на возможность генерации ситуации с данным номером хода
            new_sit = [row[:] for row in sit]  # Копируем массив
            # Меняем местами пустую ячейку с целевой
            new_sit[row][col], new_sit[new_row][new_col] = new_sit[new_row][new_col], new_sit[row][col]
            sits.append(new_sit)
    return sits



def IsGoal(sit):
    """Функция проверки на достижение целевой ситуации"""
    return sit == goal_sit


def PrntSit(sit):
    """Процедура печати ситуации"""
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


def BFS(start_sit):
    """Функция поиска в ширину"""
    visited = set()  # Множество для отслеживания посещенных ситуаций
    start_sit = Node(start_sit, None)
    queue = deque([start_sit])  # Очередь, хранящая ситуации

    while queue:
        current_sit = queue.popleft()  # Извлекаем текущую ситуацию

        if IsGoal(current_sit.value):  # Проверка на достижение цели
            break

        visited.add(tuple(tuple(row) for row in current_sit.value))

        # Генерируем и добавляем новые ситуации в очередь

        sits = NextSit(current_sit.value)
        for new_sit in sits:
            if tuple(tuple(row) for row in new_sit) not in visited:
                queue.append(Node(new_sit, current_sit))  # Добавляем новую ситуацию и путь к ней в очередь

    solution = []
    while current_sit:
        solution.append(current_sit.value)
        current_sit = current_sit.previous
    solution.reverse()
    return solution


start_sit = [[2, 0, 3],
             [7, 4, 5],
             [8, 1, 6]]

goal_sit = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

solution = BFS(start_sit)

if solution is None:
    print("Решение не найдено")
else:
    print("Решение найдено!")
    for n, sit in enumerate(solution):
        print(f'Шаг {n}')
        PrntSit(sit)
