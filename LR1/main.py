import random
import numpy as np
import matplotlib.pyplot as plt


a, b = -2, 4
ay, by = 10e9, -10e9
n = 0
list_x = np.empty(n)
list_y = np.empty(n)
step = 0.01


def define_list_x():
    global list_x
    list_x = np.empty(n)
    for i in range(n):
        rand = random.random()
        list_x[i] = rand * (b - a) + a


def function_y(x):
    return abs(x)


def define_limit_y():
    global ay, by
    for x in np.arange(a, b, step):
        y = function_y(x)
        ay = min(ay, y)
        by = max(by, y)


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
            if y == r:
                return None
            if y <= r:
                return count
            else:
                count += 1 / n


def main():
    global n, list_x, list_y
    n = int(input("Введите размерность n: "))
    define_list_x()
    list_x.sort()
    print("Вариационный ряд X:")
    print(list_x)
    list_y = np.array([function_y(x) for x in list_x])
    print("Таблица X - Y")
    for i in range(n):
        print("{:>20}    -    {}".format(list_x[i], list_y[i]))
    list_y.sort()
    print("Вариационный ряд Y:")
    print(list_y)
    define_limit_y()
    interval_y = np.arange(ay - 5, by + 5, step)
    plt.plot(interval_y, np.array([empirical_distribution_function(y) for y in interval_y]))
    plt.show()
    # plt.plot(interval_y, np.array([theoretical_distribution_function(y) for y in interval_y]))
    plt.hlines(np.array([empirical_distribution_function(y) for y in interval_y]), [0, *interval_y], [*interval_y, 4])
    plt.show()


if __name__ == '__main__':
    main()
