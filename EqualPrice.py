"""
Решение игры "Пятнашки 3х3" методом равных цен.
"""

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


# Функция проверки целевой ситуации
# Входные данные: Ситуация
def IsGoal(sit):
    return sit == goal_sit


# Процедура печати ситуации
# Входные данные: Ситуация
def PrntSit(sit):
    for i in range(3):
        print(' '.join(str(x) for x in sit[i]))
    print()


# Метод равных цен
# uniform-cost search
def UCS(situation):
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


# начальная ситуация
start_sit = [[2, 0, 3],
             [7, 4, 5],
             [8, 1, 6]]

# целевая ситуация
goal_sit = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

solution = UCS(start_sit)  # Стек для хранения пути к решению


if solution is None:
    print("Решение не найдено")
else:
    print("Решение найдено!")
    for n, sit in enumerate(solution):
        print(f'Шаг {n}')
        PrntSit(sit)

