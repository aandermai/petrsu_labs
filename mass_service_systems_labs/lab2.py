import matplotlib.pyplot as plt
import numpy as np

# * ЗАДАНИЕ 1: НАХОЖДЕНИЕ СТАЦИОНАРНОГО РАСПРЕДЕЛЕНИЯ

# Матрица переходов
P = np.array([
    [0.5, 0.1, 0.4],
    [0.1, 0.4, 0.5],
    [0.2, 0.4, 0.4]
])

A = P.T - np.eye(3)
A[2] = [1, 1, 1]
print(A)
b = np.array([0, 0, 1])
pi = np.linalg.solve(A, b)

print("Стационарное распределение:")
print(pi)

# * ЗАДАНИЕ 2: МОДЕЛИРОВАНИЕ ИЗМЕНЕНИЯ СОСТОЯНИЯ ЦЕПИ

N = 10_000 # Количество шагов
M = 5000 # Количество независимых экспериментов
checkpoints = [10, 100, 1000, 10000] # Шаги, на которых будем оценивать распределение

def simulate(start_state):
    """
    Моделирует M независимых цепей Маркова.

    start_state — начальное состояние (0, 1 или 2).
    """

    # Все цепи начинаются из одного состояния
    states = np.full(M, start_state)

    results = {}

    # Накопленные вероятности переходов
    cumulative = np.cumsum(P, axis=1)

    for step in range(1, N + 1):

        # Генерируем случайные числа от 0 до 1
        random_values = np.random.random(M)

        # Выбираем новое состояние
        states = (
            (random_values > cumulative[states, 0]).astype(int)
            + (random_values > cumulative[states, 1]).astype(int)
        )

        # Сохраняем распределение на контрольных шагах
        if step in checkpoints:
            probabilities = (
                np.bincount(states, minlength=3) / M
            )

            results[step] = probabilities

    return results


# Три начальных состояния
initial_states = [0, 1, 2]

# Запускаем моделирование
np.random.seed(42)

simulation_results = {}

for state in initial_states:
    simulation_results[state] = simulate(state)

    print(f"\nНачальное состояние: {state + 1}")

    for step, probabilities in simulation_results[state].items():
        print(
            f"Шаг {step:5d}: "
            f"{probabilities.round(6)}"
        )

plt.figure(figsize=(10, 6))

for state in initial_states:

    # Начальное распределение
    current = np.eye(3)[state]

    distances = []

    for step in range(1, N + 1):

        # Вычисляем распределение на следующем шаге
        current = current @ P

        # Расстояние до стационарного распределения
        distance = np.linalg.norm(current - pi)

        distances.append(distance)

    plt.plot(
        range(1, N + 1),
        distances,
        label=f"Начальное состояние {state + 1}"
    )

plt.xlabel("Количество шагов")
plt.ylabel("Расстояние до стационарного распределения")
plt.title("Сходимость цепи Маркова")
plt.legend()
plt.grid()
plt.yscale("log")
plt.show()

# * ЗАДАНИЕ 3: ОЦЕНКА РЕЛАКСАЦИИ

# Допустимая погрешность
epsilon = 0.01

def relaxation_time(start_state, epsilon):
    # Начальное распределение
    current = np.eye(3)[start_state]

    for step in range(1, N + 1):
        # Следующий шаг цепи
        current = current @ P

        # Расстояние до стационарного распределения
        distance = np.linalg.norm(current - pi)

        # Проверяем условие релаксации
        if distance < epsilon:
            return step

    return None


print("\nВремя релаксации:")

for state in initial_states:

    time = relaxation_time(state, epsilon)

    print(
        f"Начальное состояние {state + 1}: "
        f"{time} шагов"
    )