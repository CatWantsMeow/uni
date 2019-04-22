# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from discrete_random import DiscreteRandom


class RandomTest(object):

    def test_uniformity(self):
        raise NotImplementedError

    def test_independence(self):
        raise NotImplementedError

    def test(self):
        self.test_uniformity()
        self.test_independence()


class DiscreteRandomTest(RandomTest):

    __iterations = [
        50,
        100,
        1000,
        5000,
        10000,
        50000
    ]

    def test_uniformity(self):
        for n in self.__iterations:
            rand = DiscreteRandom(n=n)
            rand.stats()

    def test_independence(self):
        r = []
        rand = DiscreteRandom()
        for n in self.__iterations:
            s = n / 3
            z = [rand.next() for _ in xrange(n)]
            mx = sum(z) / float(n)
            dx = sum((z[i] - mx) ** 2 for i in xrange(n)) / float(n)
            mxy = sum(z[i] * z[i + s] for i in xrange(n - s)) / float(n - s)
            r.append((mxy - mx * mx) / dx)
        print 'Значения коэффициента корреляции:'
        print '\n'.join(["R = {:7.5}".format(c) for c in r])


if __name__ == '__main__':
    DiscreteRandomTest().test()