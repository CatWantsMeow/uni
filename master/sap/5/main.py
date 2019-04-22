# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d as _
from scipy import optimize


# исходная функция
def f(x):
    return 4 * x[0] ** 2 + 2 * x[0] ** 2 * x[1] ** 2 + 4 * x[1] ** 2 + 7


# градиент исходной функции
def gradf(x):
    gx1 = 4 * 2 * x[0] + 2 * x[0] * x[1] ** 2
    gx2 = 2 * x[0] ** 2 * x[1] + 2 * 4 * x[1]
    return np.array([gx1, gx2])


def main():
    # поиск минимума функции
    x_min, x_grad = optimize.fmin_cg(f, np.array([4.5, 4.6]), fprime=gradf, retall=True)

    # инициализация значений для графиков
    interval = np.arange(-5, 5, 0.1)
    x = np.array([[e] * len(interval) for e in interval])
    y = np.array([[e for e in interval]] * len(interval))
    z = np.array([[f((u, v)) for u in interval] for v in interval])

    # график поверхности функции
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(x, y, z, color=(0, 0, 0.8, 0.2), label='f(u, v)')

    # график изменения градиента функции
    ax.plot(
        [x[0] for x in x_grad],
        [x[1] for x in x_grad],
        [f(x) for x in x_grad],
        '--.',
        color=(0.5, 0, 0, 1), linewidth=1, markersize=4, label='grad(f(u, v))'
    )

    # начальная точка и точка минимума функции
    ax.scatter(
        x_grad[0][0], x_grad[0][1], f(x_grad[0]), 'o',
        color='blue', label='(x0, y0)', linewidths=4
    )
    ax.scatter(
        x_min[0], x_min[0], f(x_min), 'o',
        color='green', label='(xmin, ymin)', linewidths=4
    )

    # вывод графиков на экран и сохранение в файл
    ax.legend(loc='lower center')
    plt.show()
    fig.savefig('plot.png')


if __name__ == '__main__':
    main()
