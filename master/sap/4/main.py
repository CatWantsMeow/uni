# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d


# исходная функция
def f(x):
    return np.sin(x ** 2) + np.cos(x ** 2)


def main():
    # инициализация вектора иксов и подсчет значений f(x)
    x = np.linspace(-4, 4, 20)
    y = f(x)

    # получение интерполяций функции с помощью трех видов сплайна
    f1 = interp1d(x, y, kind='slinear')
    f2 = interp1d(x, y, kind='quadratic')
    f3 = interp1d(x, y, kind='cubic')

    # генерация точек для графиков
    xx = np.linspace(-4, 4, 1000)

    # график исходной функции
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_title('Initial Function')
    ax1.plot(xx, f(xx), linewidth=2)

    # график интерполяции с помошью линейного сплайна
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_title('Linear Interpolation')
    ax2.plot(xx, f(xx), '-.', color=(0, 0, 0, 0.5))
    ax2.plot(xx, f1(xx), linewidth=1, color=(0.5, 0, 0))

    # график интерполяции с помощью квадратного сплайна
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_title('Quadratic Interpolation')
    ax3.plot(xx, f(xx), '-.', color=(0, 0, 0, 0.5))
    ax3.plot(xx, f2(xx), linewidth=1, color=(0, 0.5, 0))

    # график интерполяции с помошью кубического сплайна
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_title('Cubic Interpolation')
    ax4.plot(xx, f(xx), '-.', color=(0, 0, 0, 0.5))
    ax4.plot(xx, f3(xx), linewidth=1, color=(0, 0, 0.5))

    # вывод графиков на экран
    plt.show()


if __name__ == '__main__':
    main()
