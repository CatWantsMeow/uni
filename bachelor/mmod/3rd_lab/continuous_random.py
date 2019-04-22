# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from time import time
from numpy import arange
from math import log, exp
from matplotlib import pyplot as plot
from random import Random as PyRandom


class Random(object):

    def __init__(self, seed=None, n=10000):
        self._current = seed or int(time() * 10000)
        self._n = n

    def density(self, x):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError

    def stats(self):
        values = [self.next() for _ in xrange(self._n)]
        weights = [10.0 / self._n for _ in xrange(self._n)]
        plot.hist(values, 100, weights=weights, facecolor='g', alpha=0.4)

        x_values = arange(min(values), max(values), 0.001)
        y_values = [self.density(x) for x in x_values]
        plot.plot(x_values, y_values, color='b', lw=2)

        plot.grid(True)
        plot.show()


class ExponentialRandom(Random):

    __lambda = 1

    def __init__(self, seed=None, n=10000):
        super(ExponentialRandom, self).__init__(seed, n)
        self._rand = PyRandom(seed)

    def density(self, x):
        return self.__lambda * exp(0 - self.__lambda * x)

    def next(self):
        x = self._rand.random()
        return 0 - log(1 - x) / self.__lambda


if __name__ == '__main__':
    ExponentialRandom().stats()