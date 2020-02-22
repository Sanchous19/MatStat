import numpy as np
import random
import math
from scipy import stats


a, b = -2, 4
ay, by = 10e9, -10e9
n = 0
list_y = np.empty(n)


def function_y(x):
    return abs(x)


def theoretical_distribution_function(y):
    if y < 0:
        return 0
    if 0 <= y <= 2:
        return y / 3
    elif 2 < y < 4:
        return 1 / 3 + y / 6
    else:
        return 1


def define_list_y():
    global list_y
    list_y = np.empty(n)
    for i in range(n):
        rand = random.random()
        x = rand * (b - a) + a
        list_y[i] = function_y(x)
    list_y.sort()


def pirson_criterion_statistics():
    result = 0
    if n <= 100:
        m = int(math.sqrt(n))
    elif n % int(3 * math.log(n)) == 0:
        m = int(3 * math.log(n))
    elif n % int(4 * math.log(n)) == 0:
        m = int(4 * math.log(n))
    else:
        m = int(2 * math.log(n))
    num_interval = m
    remainder = n % m
    if remainder >= m // 2:
        num_interval += 1
    left = list_y[0]
    for i in range(num_interval):
        if i == num_interval - 1:
            right = list_y[n - 1]
        else:
            right = (list_y[(n // m) * (i + 1)] + list_y[(n // m) * (i + 1) - 1]) / 2
        theoretical_probability = theoretical_distribution_function(right) - theoretical_distribution_function(left)
        left = right
        if i != num_interval - 1:
            probability = (n // m) / n
        elif remainder >= m // 2:
            probability = remainder / n
        else:
            probability = (n // m + remainder) / n
        result += ((probability - theoretical_probability) ** 2) / theoretical_probability
    result *= n
    k = num_interval - 1 - 0
    return result, k


def kolmogorov_criterion_statistics():
    d_minus, d_plus = 0, 0
    for i in range(n):
        d_minus = max(d_minus, abs(theoretical_distribution_function(list_y[i]) - ((i + 1) - 1) / n))
        d_plus = max(d_plus, abs((i + 1) / n) - theoretical_distribution_function(list_y[i]))
    return math.sqrt(n) * max(d_minus, d_plus)


def mizes_criterion_statistics():
    result = 1 / (12 * n)
    for i in range(n):
        result += (theoretical_distribution_function(list_y[i]) - ((i + 1) - 0.5) / n) ** 2
    return result


def result_of_checking(is_true):
    if is_true:
        print("Нет основания отклонять гипотезу H0.")
    else:
        print("Отклоняем гипотезу H0.")


def main():
    global n
    print("Критерий Пирсона")
    n = 200
    define_list_y()
    value, k = pirson_criterion_statistics()
    print("Значение критерия Пирсона:", value)
    result_of_checking(value < stats.chi2.ppf(1-0.05, k))
    print()

    print("Критерий Колмогорова")
    n = 30
    define_list_y()
    value = kolmogorov_criterion_statistics()
    print("Значение критерия Колмогорова:", value)
    result_of_checking(value <= stats.kstwobign.ppf(1-0.05))
    print()

    print("Критерий Мизеса")
    n = 50
    define_list_y()
    value = mizes_criterion_statistics()
    print("Значение критерия Мизеса:", value)
    result_of_checking(value <= 0.744)


if __name__ == '__main__':
    main()
