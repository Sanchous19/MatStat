import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
from scipy.stats import chi2


a, b = -2, 4
m, d = (5 / 3), (11 / 9)
n = 0
list_y = np.empty(n)


def function_y(x):
    return abs(x)


def define_list_y():
    global list_y
    list_y = np.empty(n)
    for i in range(n):
        rand = random.random()
        x = rand * (b - a) + a
        list_y[i] = function_y(x)
    list_y.sort()


def expected_value():
    return np.sum(list_y) / n


def variance():
    m = expected_value()
    return np.sum((list_y - m) ** 2) / (n - 1)


def expected_value_confidence_interval(a, is_known_variance):
    m = expected_value()
    if is_known_variance:
        s = math.sqrt(d)
        variance_str = ' с известной дисперсией'
    else:
        s = math.sqrt(variance())
        variance_str = ''
    stud_val = t.ppf(1 - a / 2, n - 1)
    print('Доверительный интервал для матожидания:', (m - s * stud_val / math.sqrt(n - 1)), '<= m <=',
          (m + s * stud_val / math.sqrt(n - 1)), 'со значимостью', 1 - a, variance_str)


def draw_m_interval_from_a():
    xlist = np.arange(0, 1, 0.001)
    ylist = []
    for a in xlist:
        s = math.sqrt(variance())
        stud_val = t.ppf(1 - a / 2, n - 1)
        ylist.append(2 * s * stud_val / math.sqrt(n - 1))
    plt.plot(1 - xlist, ylist, label='Без дисперсии')

    ylist = []
    for a in xlist:
        s = math.sqrt(d)
        stud_val = t.ppf(1 - a / 2, n - 1)
        ylist.append(2 * s * stud_val / math.sqrt(n - 1))
    plt.plot(1 - xlist, ylist, label='С дисперсией')

    plt.title("Зависимость величины доверительного интервала\n от уровня значимости")
    plt.legend(loc='upper left')
    plt.show()


def draw_m_interval_from_n(a):
    global n
    a = 1 - a
    xlist = np.arange(10, 200, 1)
    ylist = []
    for x in xlist:
        n = x
        define_list_y()
        s = math.sqrt(variance())
        stud_val = t.ppf(1 - a / 2, x - 1)
        ylist.append(2 * s * stud_val / math.sqrt(x - 1))
    plt.plot(xlist, ylist, label='Без дисперсии')

    ylist = []
    for x in xlist:
        n = x
        define_list_y()
        s = math.sqrt(d)
        stud_val = t.ppf(1 - a / 2, x - 1)
        ylist.append(2 * s * stud_val / math.sqrt(x - 1))
    plt.plot(xlist, ylist, label='С дисперсией')

    plt.title("Зависимость величины доверительного интервала\n от объёма выборки с доверительным значением"
              + str(1 - a))
    plt.legend(loc='upper left')
    plt.show()


def variance_confidence_interval(a, is_known_expected_value):
    if is_known_expected_value:
        s = math.sqrt(np.sum((list_y - m) ** 2) / (n - 1))
        variance_str = 'с известным матожиданием'
        freedom_degree = n
    else:
        s = math.sqrt(variance())
        variance_str = ''
        freedom_degree = n - 1
    chi2_val0 = chi2.isf((1 - (1 - a)) / 2, freedom_degree)
    chi2_val1 = chi2.isf((1 + (1 - a)) / 2, freedom_degree)
    print("Доверительный интервал для дисперсии:", (n * (s ** 2) / chi2_val0), "<= D <=", (n * (s ** 2) / chi2_val1),
          "со значимостью", 1 - a, variance_str)


def draw_d_interval_from_a():
    xlist = np.arange(0.001, 1, 0.001)
    ylist = []
    for a in xlist:
        s = math.sqrt(variance())
        chi2_val0 = chi2.isf((1 - (1 - a)) / 2, n - 1)
        chi2_val1 = chi2.isf((1 + (1 - a)) / 2, n - 1)
        ylist.append((n * (s ** 2) / chi2_val1) - (n * (s ** 2) / chi2_val0))
    plt.plot(1 - xlist, ylist, label='Без матожидания')

    ylist = []
    for a in xlist:
        s = math.sqrt(np.sum((list_y - m) ** 2) / (n - 1))
        chi2_val0 = chi2.isf((1 - (1 - a)) / 2, n)
        chi2_val1 = chi2.isf((1 + (1 - a)) / 2, n)
        ylist.append((n * (s ** 2) / chi2_val1) - (n * (s ** 2) / chi2_val0))
    plt.plot(abs(1 - xlist), ylist, label='С матожиданием')

    plt.title("Зависимость величины доверительного интервала\n от уровня значимости")
    plt.legend(loc='upper left')
    plt.show()


def draw_d_interval_from_n(a):
    global n
    a = 1 - a
    xlist = np.arange(10, 200, 1)
    ylist = []
    for x in xlist:
        n = x
        define_list_y()
        s = math.sqrt(variance())
        chi2_val0 = chi2.isf((1 - (1 - a)) / 2, n - 1)
        chi2_val1 = chi2.isf((1 + (1 - a)) / 2, n - 1)
        ylist.append((n * (s ** 2) / chi2_val1) - (n * (s ** 2) / chi2_val0))
    plt.plot(xlist, ylist, label='Без матожидания')

    ylist = []
    for x in xlist:
        n = x
        define_list_y()
        s = math.sqrt(np.sum((list_y - m) ** 2) / (n - 1))
        chi2_val0 = chi2.isf((1 - (1 - a)) / 2, n)
        chi2_val1 = chi2.isf((1 + (1 - a)) / 2, n)
        ylist.append((n * (s ** 2) / chi2_val1) - (n * (s ** 2) / chi2_val0))
    plt.plot(xlist, ylist, label='С матожиданием')

    plt.title("Зависимость величины доверительного интервала\n от объёма выборки с доверительным значением"
              + str(1 - a))
    plt.legend(loc='upper left')
    plt.show()


def main():
    global n
    n = 20
    define_list_y()
    print('Точечная оценка матожидания', expected_value())
    print('Точечная оценка дисперсии', variance())
    print()
    expected_value_confidence_interval(0.01, False)
    expected_value_confidence_interval(0.03, False)
    expected_value_confidence_interval(0.05, False)
    print()
    expected_value_confidence_interval(0.01, True)
    expected_value_confidence_interval(0.03, True)
    expected_value_confidence_interval(0.05, True)
    draw_m_interval_from_a()
    draw_m_interval_from_n(0.98)
    print()
    n = 20
    define_list_y()
    variance_confidence_interval(0.01, False)
    variance_confidence_interval(0.03, False)
    variance_confidence_interval(0.05, False)
    print()
    variance_confidence_interval(0.01, True)
    variance_confidence_interval(0.03, True)
    variance_confidence_interval(0.05, True)
    draw_d_interval_from_a()
    draw_d_interval_from_n(0.98)


if __name__ == '__main__':
    main()