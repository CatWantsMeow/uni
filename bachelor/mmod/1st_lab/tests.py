# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from matplotlib import pyplot as plot
from argparse import ArgumentParser
from random_values import (
    MultiplicativeCongruentialRandom,
    MiddleSquareRandom,
    TriangleRandom,
    GaussRandom
)


class RandomMethodTest(object):

    __k = 50
    __iterations = [10, 100, 1000, 10000, 100000]

    def __init__(self, rand_class):
        self._rand_class = rand_class

    def test_uniformity(self):
        rand = self._rand_class()
        for n in self.__iterations:
            z = [rand.next() for _ in xrange(n)]
            plot.hist(z, self.__k, weights=[1.0 / n for i in xrange(n)])
            plot.show()

    def test_independence(self):
        r = []
        rand = self._rand_class()
        for n in self.__iterations:
            s = n / 3
            z = [rand.next() for _ in xrange(n)]
            mx = sum(z) / float(n)
            dx = sum((z[i] - mx) ** 2 for i in xrange(n)) / float(n)
            mxy = sum(z[i] * z[i + s] for i in xrange(n - s)) / float(n - s)
            r.append((mxy - mx * mx) / dx)
        print 'Значения коэффициента корреляции:'
        print '\n'.join(["{:.5}".format(c) for c in r])

    def test(self):
        self.test_uniformity()
        self.test_independence()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-ms', '--middle-square', action='store_true')
    parser.add_argument('-mc', '--multiplicative-congruential', action='store_true')
    parser.add_argument('-g', '--gauss', action='store_true')
    parser.add_argument('-t', '--triangle', action='store_true')
    args = parser.parse_args()

    if args.middle_square:
        RandomMethodTest(MiddleSquareRandom).test()
    if args.multiplicative_congruential:
        RandomMethodTest(MultiplicativeCongruentialRandom).test()
    if args.triangle:
        RandomMethodTest(TriangleRandom).test()
    if args.gauss:
        RandomMethodTest(GaussRandom).test()

