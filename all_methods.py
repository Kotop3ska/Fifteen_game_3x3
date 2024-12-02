from collections import deque
from random import choice
from prettytable import PrettyTable


def DFS(sit, level_limit, level=0):
    global N_DFS
    """Функция поиска в глубину"""
    if IsGoal(sit):  # проверка на достижение цели
        solution_DFS.append(sit)
        return True

    if level == level_limit:  # проверка на достижение ограничения
        return False

    for number in range(1, 5):
        new_sit = NextSit(sit, number)
        N_DFS += 1
        if new_sit and new_sit not in solution_DFS:  # Проверка на возможность ситуации при данном номере хода
            solution_DFS.append(sit)  # Добавляем текущую ситуацию в стек
            if DFS(new_sit, level_limit, level + 1):  # Рекурсивно вызываем DFS
                return True
            solution_DFS.pop()  # Убираем ситуацию, если не привела к решению

    return False


"""Метод поиска по градиенту"""


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


def GradeSearch(sit, level_limit, level=0):
    """Функция поиска в глубину"""
    global N_GRAD
    if IsGoal(sit):  # проверка на достижение цели
        solution_GRAD.append(sit)
        return True

    if level == level_limit:  # проверка на достижение ограничения
        return False

    for new_sit in Appritiation(sit):
        if new_sit and new_sit not in solution_GRAD:  # Проверка на возможность ситуации при данном номере хода
            N_GRAD += 1
            solution_GRAD.append(sit)  # Добавляем текущую ситуацию в стек
            if GradeSearch(new_sit, level_limit, level + 1):  # Рекурсивно вызываем DFS
                return True
            solution_GRAD.pop()  # Убираем ситуацию, если не привела к решению

    return False


"""Метод поиска в ширину"""


class Node:
    def __init__(self, sit, prev):
        self.value = sit
        self.previous = prev


def BFS(start_sit):
    """Функция поиска в ширину"""
    global N_BFS
    visited = set()  # Множество для отслеживания посещенных ситуаций
    start_sit = Node(start_sit, None)
    queue = deque([start_sit])  # Очередь, хранящая ситуации

    while queue:
        current_sit = queue.popleft()  # Извлекаем текущую ситуацию

        if IsGoal(current_sit.value):  # Проверка на достижение цели
            break

        visited.add(tuple(tuple(row) for row in current_sit.value))

        # Генерируем и добавляем новые ситуации в очередь
        for number in range(1, 5):
            new_sit = NextSit(current_sit.value, number)  # Генерируются для ситуации следующие ходы
            N_BFS += 1
            if new_sit:
                if tuple(tuple(row) for row in new_sit) not in visited:
                    queue.append(Node(new_sit, current_sit))  # Добавляем новую ситуацию и путь к ней в очередь

    solution = []
    while current_sit:
        solution.append(current_sit.value)
        current_sit = current_sit.previous
    solution.reverse()
    return solution


"""Метод равных цен"""


# Класс для хранения вершины дерева решений
# для поиска в ширину
class SitNode:
    def __init__(self, sit, prev, cost):
        self.value = sit    # Хранит ситуацию для текущей вершины
        self.previous = prev    # Хранит предыдущую ситуацию
        self.cost = cost    # Стоимость действий от начальной вершины


# Класс, реализующий структуру кучи с поддержкой минимума
# В куче хранятся объекты класса Sit_Node
class MinHeap:
    def __init__(self):
        self.heap = [0]
        self.size = 0

    def insert(self, x):
        self.heap.append(x)
        self.size += 1

    def indMaxChild(self, i):
        if i * 2 + 1 > self.size:
            return i * 2
        if self.heap[i * 2].cost < self.heap[i * 2 + 1].cost:
            return i * 2
        return i * 2 + 1

    def shiftUp(self, i):
        while i // 2 > 0 and self.heap[i].cost < self.heap[i // 2].cost:
            self.heap[i], self.heap[i // 2] = self.heap[i // 2], self.heap[i]
            i = i // 2

    def shiftDown(self, i):
        while i * 2 <= self.size:
            j = self.indMaxChild(i)
            if self.heap[i].cost > self.heap[j].cost:
                self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
            i = j

    def extract(self):
        if self.size is None:
            return None
        removed = self.heap[1]
        self.heap[1] = self.heap[self.size]
        self.size = self.size - 1
        self.heap.pop()
        self.shiftDown(1)
        return removed


# Метод равных цен
# uniform-cost search
def UCS(situation):
    global N_UCS
    node = SitNode(situation, None, 0)
    current_sit = node  # Создается объект класса Sit - корень дерева
    heap = MinHeap()  # Куча в которую будут добавляться ситуации
    heap.insert(current_sit)
    visited = [current_sit.value]  # Список для хранения посещенных вершин
    while True:  # Поиск в ширину через цикл
        current_sit = heap.extract()  # Достается ситуация из очереди с минимальной стоимостью
        if IsGoal(current_sit.value):
            break
        for number in range(1, 5):
            new_sit = NextSit(current_sit.value, number)  # Генерируются для ситуации следующие ходы
            N_UCS += 1
            if new_sit and new_sit not in visited:  # Проверка, что ситуация еще не была посещена
                visited.append(new_sit)
                # Добавляется в кучу объект класса SitNode и указываем в качестве предыдущей вершины current_sit
                # В текущей стоимости ситуации мы добавляем разницу между Манхэттонскими расстояниями
                # для следующей и текущей ситуации, что является стоимостью перехода к следующей ситуации
                heap.insert(SitNode(new_sit, current_sit, current_sit.cost + Grade(new_sit) - Grade(current_sit.value)+1))
    solution = []
    # Формируем путь решения получаяя предыдущую ситуацию для каждой
    while current_sit is not None:
        solution.append(current_sit.value)
        current_sit = current_sit.previous
    solution.reverse()  # Переворачиваем список пути
    return solution


"""Mетод двустороннего поиска"""


# Класс, представляющий собой вершину дерева решений
class Sit:
    def __init__(self, sit, prev):
        self.value = sit    # Хранит ситуацию
        self.previous = prev    # Хранит предыдущую вершину


# Функция, реализующая метод двунаправленного поиска
# Входные данные: Начальная и Целевая ситуации
def TwoSidedSearch(situation, goal_situation):
    global N_TSS
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
                N_TSS += 1
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
                N_TSS += 1
                if new_sit and new_sit not in visited_goal:  # Проверка, что ситуация еще не была посещена
                    visited_goal.append(new_sit)
                    temp.append(Sit(new_sit, sit))  # Добавляем в список
        level_goal = temp


"""Вспомогательные функции"""


# Процедура печати ситуации
# Входные данные: Ситуация
def PrntSit(sit):
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


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

# Функция для нахождения пустой ячейки (0)
# Входные данные: Ситуация
def FindZero(sit):
    for i in range(3):
        for j in range(3):
            if sit[i][j] == 0:
                return i, j
    return None


# Функция проверки целевой ситуации
# Входные данные: Ситуация
def IsGoal(sit):
    return sit == goal_sit


# Функция оценки приближенности ситуации к целевой
# На вход получает ситуацию
# Возвращает оценку данной ситуации, т.е. на сколько ходов она далека от терминальной ситуации
def Grade(sit):
    situation = [sit[i][j] for i in range(len(sit)) for j in range(len(sit))]
    grade = 0
    # Просчет манхэтенского расстояния для каждой ячейки
    for i in range(len(situation)):
        if situation[i] != 0:
            grade += abs((i // 3 + 1) - ((situation[i] - 1) // 3 + 1)) + abs((i % 3) - ((situation[i] - 1) % 3))
    # Возвращает оценку для ситуации
    return grade


def GenMatr(matr):
    sit = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            sit[i][j] = matr.pop(0)
    return sit


# Генерация решаемой начальной ситуации
def InputGeneration(n):
    input_matrix = []
    numbers = [x for x in range(n)]
    for i in range(n):
        random_number = choice(numbers)
        numbers.remove(random_number)
        input_matrix.append(random_number)
    inversions = 0              # Проверка решаемости ситуации через инверсии и их четность
    for num in range(n):
        for next_num in range(num, n):
            if input_matrix[num] > input_matrix[next_num] and input_matrix[next_num] != 0:
                inversions += 1
    if inversions % 2 == 1:
        num1 = input_matrix.index(n - 1)
        num2 = input_matrix.index(n - 2)
        input_matrix[num1] = n - 2
        input_matrix[num2] = n - 1
    sit = GenMatr(input_matrix)
    return sit


"""Основная программа"""
# целевая ситуация
goal_sit = InputGeneration(9)

start_sit = [[2, 0, 3],
             [7, 4, 5],
             [8, 1, 6]]

"""В глубину"""
level_limit = 20
solution_DFS = []
N_DFS = 0

if not DFS(start_sit, level_limit):
    print(f"Решение не найдено при ограничении в {level_limit}")
else:
    D_DFS = level_limit
    L_DFS = len(solution_DFS)
    R_DFS = int(N_DFS / L_DFS)
    W_DFS = N_DFS**(1 / L_DFS)


"""По градиенту"""
solution_GRAD = []
N_GRAD = 0
if not GradeSearch(start_sit, level_limit):
    print(f"Решение не найдено при ограничении в {level_limit}")
else:
    D_GRAD = level_limit
    L_GRAD = len(solution_DFS)
    R_GRAD = int(N_GRAD / L_GRAD)
    W_GRAD = N_GRAD**(1 / L_GRAD)

"""В ширину"""
N_BFS = 0
solution_BFS = BFS(start_sit)
L_BFS = len(solution_BFS)
D_BFS = L_BFS
R_BFS = int(N_BFS / L_BFS)
W_BFS = N_BFS**(1 / L_BFS)


"""Равных цен"""
N_UCS = 0
solution_UCS = UCS(start_sit)
L_UCS = len(solution_UCS)
D_UCS = L_UCS
R_UCS = int(N_UCS / L_UCS)
W_UCS = N_UCS**(1 / L_UCS)


"""Двунаправленный"""
N_TSS = 0
solution_TSS = TwoSidedSearch(start_sit, goal_sit)
L_TSS = len(solution_TSS)
D_TSS = L_TSS
R_TSS = int(N_TSS / L_TSS)
W_TSS = N_TSS**(1 / L_TSS)


mytable = PrettyTable()
mytable.field_names = ["Метод", "Глубина поиска", "Длина пути", "Общее число порожденных вершин",
                       "Разветвленность дерева", "Направленность поиска"]

mytable.add_row(["В глубину", D_DFS, L_DFS, N_DFS, R_DFS, W_DFS])
mytable.add_row(["По градиенту", D_GRAD, L_GRAD, N_GRAD, R_GRAD, W_GRAD])
mytable.add_row(["В ширину", D_BFS, L_BFS, N_BFS, R_BFS, W_BFS])
mytable.add_row(["Равных цен", D_UCS, L_UCS, N_UCS, R_UCS, W_UCS])
mytable.add_row(["Двунаправленный", D_TSS, L_TSS, N_TSS, R_TSS, W_TSS])
print(mytable)

