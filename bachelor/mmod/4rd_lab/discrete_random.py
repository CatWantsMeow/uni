# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from collections import OrderedDict
from time import time
from numpy import arange
from math import log, exp
from matplotlib import pyplot as plot
from random import Random as PyRandom


class Random(object):

    _distribution = None

    def __init__(self, seed=None, n=10000):
        self._current = seed or int(time() * 10000)
        self._n = n

    def next(self):
        raise NotImplementedError

    def stats(self):
        values = [self.next() for _ in xrange(self._n)]
        weights = [1.0 / self._n for _ in xrange(self._n)]
        plot.hist(values, 100, weights=weights, facecolor='g', alpha=0.7)

        x_values = self._distribution.keys()
        y_values = [self._distribution.values()[0]]
        for i in xrange(1, len(self._distribution.values())):
            y_values.append(self._distribution.values()[i] - self._distribution.values()[i - 1])
        plot.plot(x_values, y_values, color='b', lw=1, alpha=0.7, marker='.', markeredgewidth=5)

        plot.grid(True)
        plot.show()


class DiscreteRandom(Random):

    _distribution = OrderedDict((
        (1.0, 0.125),
        (1.3, 0.165),
        (2.3, 0.325),
        (2.9, 0.5),
        (3.6, 0.51),
        (4.1, 0.59),
        (4.3, 0.62),
        (4.7, 0.66),
        (5.9, 0.74),
        (7.0, 0.88),
        (8.4, 0.94),
        (10.0, 1.0),
    ))

    def __init__(self, seed=None, n=10000):
        super(DiscreteRandom, self).__init__(seed, n)
        self._rand = PyRandom(seed)

    def next(self):
        x = self._rand.random()
        for y, p in self._distribution.iteritems():
            if x < p:
                return y


if __name__ == '__main__':
    DiscreteRandom().stats()