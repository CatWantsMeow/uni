# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import numpy as np
from random import randint, random
from matplotlib import pyplot as plot
from mpl_toolkits.mplot3d import Axes3D


class ComplexDiscreteRandom(object):

    @staticmethod
    def __generate_p(n, m):
        while True:
            p = [[randint(0, 20) / (n * m * 10.0) for _ in xrange(m)] for _ in xrange(n)]
            if sum(sum(row) for row in p) == 1:
                return p

    @staticmethod
    def __generate_x(n):
        x = []
        while len(x) < n:
            value = randint(0, 100) / 100.0
            if value not in x:
                x.append(value)
        x.sort()
        return x

    def __init__(self, n=5, m=5, x=None, y=None, p=None, rounds=100000):
        self.x = x or self.__generate_x(n)
        self.y = y or self.__generate_x(n)
        self.p = p or self.__generate_p(n, m)
        self._rounds = rounds

    @staticmethod
    def __imitate(p):
        x = random()
        i = 0
        while x > sum(p[:i + 1]):
            i += 1
        return i

    def next(self):
        k = self.__imitate([sum(row) for row in self.p])
        s = self.__imitate([float(p) / sum(self.p[k]) for p in self.p[k]])
        return self.x[k], self.y[s]

    def stats(self):
        x, y = [], []
        for i in xrange(self._rounds):
            values = self.next()
            x.append(values[0])
            y.append(values[1])

        fig = plot.figure()
        ax = fig.add_subplot(111, projection='3d')
        weights = [1.0 / self._rounds for _ in xrange(self._rounds)]
        hist, x_edges, y_edges = np.histogram2d(x, y, bins=len(self.x), range=[[0, 1], [0, 1]], weights=weights)

        x_pos, y_pos = np.meshgrid(x_edges[:-1], y_edges[:-1])
        x_pos = x_pos.flatten('F')
        y_pos = y_pos.flatten('F')
        z_pos = np.zeros_like(x_pos)

        dx = 0.045 * np.ones_like(z_pos)
        dy = dx.copy()
        dz = hist.flatten()
        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color='b', zsort='average', alpha=0.8)
        plot.show()


if __name__ == '__main__':
    rand = ComplexDiscreteRandom()
    rand.stats()