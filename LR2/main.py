import math
import random
import numpy as np
import matplotlib.pyplot as plt


a, b = -2, 4
ay, by = 10e9, -10e9
n, m = 0, 0
list_y = np.empty(n)
step = 0.01
delta = 0
interval_right_board = np.empty(m)
v_interval = np.empty(m)
num_interval = 0
probability_right_board = np.empty(m)
probabilities = np.empty(m)


def define_list_y():
    global list_y
    list_y = np.empty(n)
    for i in range(n):
        rand = random.random()
        x = rand * (b - a) + a
        list_y[i] = function_y(x)
    list_y.sort()


def function_y(x):
    return abs(x)


def define_limit_y():
    global ay, by
    for x in np.arange(a, b, step):
        y = function_y(x)
        ay = min(ay, y)
        by = max(by, y)


def theoretical_distribution_density(y):
    if 0 <= y <= 2:
        return 1 / 3
    elif 2 <= y <= 4:
        return 1 / 6
    else:
        return 0


def define_v_interval():
    global delta, interval_right_board, v_interval
    interval_right_board = np.empty(m)
    v_interval = np.empty(m)
    delta = (list_y[n - 1] - list_y[0]) / m
    right = list_y[0]
    j = 0
    for i in range(m):
        right += delta
        interval_right_board[i] = right
        v = 0.5 if list_y[j] == right else 0
        while j < n and list_y[j] < right:
            v += 1
            j += 1
        if j < n and list_y[j] == right:
            v += 1 if j == n - 1 else 0.5
        v_interval[i] = v


def empirical_interval_distribution_density(y):
    if y < list_y[0] or y > list_y[n - 1]:
        return 0
    else:
        for i in range(m):
            if y <= interval_right_board[i]:
                return v_interval[i] / (n * delta)


def show_interval_poligon():
    y_interval = np.empty(m)
    for i in range(m):
        if i == 0:
            y_interval[i] = (list_y[0] + interval_right_board[i]) / 2
        else:
            y_interval[i] = (interval_right_board[i] + interval_right_board[i - 1]) / 2
    plt.plot(y_interval, v_interval / (n * delta))
    plt.show()


def define_probabilities():
    global probability_right_board, probabilities, num_interval
    num_interval = m
    remainder = n % m
    if remainder >= m // 2:
        num_interval += 1
    probability_right_board = np.empty(num_interval)
    probabilities = np.empty(num_interval)
    for i in range(num_interval):
        if i == num_interval - 1:
            probability_right_board[i] = list_y[n - 1]
        else:
            probability_right_board[i] = (list_y[(n // m) * (i + 1)] +
                                          list_y[(n // m) * (i + 1) - 1]) / 2
        if i == 0:
            interval = probability_right_board[0] - list_y[0]
        else:
            interval = probability_right_board[i] - probability_right_board[i - 1]
        if i != num_interval - 1:
            probabilities[i] = (n // m) / (n * interval)
        elif remainder >= m // 2:
            probabilities[i] = remainder / (n * interval)
        else:
            probabilities[i] = (n // m + remainder) / (n * interval)


def empirical_probability_distribution_density(y):
    if y < list_y[0] or y > list_y[n - 1]:
        return 0
    else:
        for i in range(num_interval):
            if y <= probability_right_board[i]:
                return probabilities[i]


def show_probability_poligon():
    y_interval = np.empty(num_interval)
    for i in range(num_interval):
        if i == 0:
            y_interval[i] = (list_y[0] + probability_right_board[i]) / 2
        else:
            y_interval[i] = (probability_right_board[i] + probability_right_board[i - 1]) / 2
    plt.plot(y_interval, probabilities)
    plt.show()


def theoretical_distribution_function(y):
    if y < 0:
        return 0
    if 0 <= y <= 2:
        return y / 3
    elif 2 < y < 4:
        return 1 / 3 + y / 6
    else:
        return 1


def empirical_distribution_function(y):
    if y > list_y[n - 1]:
        return 1
    else:
        count = 0
        for r in list_y:
            if y <= r:
                return count
            else:
                count += 1 / n


def main():
    global n, m, list_y
    n = int(input("Введите размерность n: "))
    if n <= 100:
        m = int(math.sqrt(n))
    elif n % int(3 * math.log(n)) == 0:
        m = int(3 * math.log(n))
    elif n % int(4 * math.log(n)) == 0:
        m = int(4 * math.log(n))
    else:
        m = int(2 * math.log(n))
    define_list_y()
    print("Вариационный ряд Y:")
    print(list_y)
    define_limit_y()
    y_interval = np.arange(ay - 1, by + 1, step)
    define_v_interval()
    plt.plot(y_interval, np.array([empirical_interval_distribution_density(y) for y in y_interval]))
    plt.plot(y_interval, np.array([theoretical_distribution_density(y) for y in y_interval]))
    plt.show()
    show_interval_poligon()
    define_probabilities()
    plt.plot(y_interval, np.array([empirical_probability_distribution_density(y) for y in y_interval]))
    plt.plot(y_interval, np.array([theoretical_distribution_density(y) for y in y_interval]))
    plt.show()
    show_probability_poligon()
    plt.plot(y_interval, np.array([empirical_distribution_function(y) for y in y_interval]))
    plt.plot(y_interval, np.array([theoretical_distribution_function(y) for y in y_interval]))
    plt.show()


if __name__ == '__main__':
    main()
