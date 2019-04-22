# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from copy import copy

from complex_random import ComplexDiscreteRandom


class ComplexDiscreteRandomTest(object):

    __iterations = [
        500,
        1000,
        5000,
        10000,
        50000,
        100000,
        500000
    ]

    def test_uniformity(self):
        n = 5
        m = 5
        rand = ComplexDiscreteRandom(n, m)
        for rounds in self.__iterations:
            p = [copy([0] * m) for _ in xrange(n)]
            for _ in xrange(rounds):
                x, y = rand.next()
                p[rand.x.index(x)][rand.y.index(y)] += 1.0 / rounds
            print sum(sum(abs(p[i][j] - rand.p[i][j]) for j in xrange(m)) for i in xrange(n))


if __name__ == '__main__':
    ComplexDiscreteRandomTest().test_uniformity()