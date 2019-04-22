# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import random
from numpy import arange


class RandomEvent(object):

    def imitate(self):
        raise NotImplementedError


class SimpleRandomEvent(RandomEvent):

    def __init__(self, p):
        self._p = p

    def imitate(self):
        x = random()
        return x <= self._p


class ComplexRandomEvent(RandomEvent):

    def __init__(self, pa, pb):
        self._pa = pa
        self._pb = pb

    def imitate(self):
        x1 = random()
        x2 = random()
        a = x1 <= self._pa
        b = x2 <= self._pb
        return a, b


class ComplexDependentRandomEvent(RandomEvent):

    def __init__(self, pa, pb, pba):
        self._pa = pa
        self._pb = pb
        self._pba = pba
        self._pbna = (pb - pba * pa) / (1 - pa)

    def imitate(self):
        x1 = random()
        x2 = random()
        a = (x1 <= self._pa)
        b = (a and (x2 <= self._pba)) or (not a and (x2 <= self._pbna))
        return a, b


class CompleteGroupRandomEvent(RandomEvent):

    def __init__(self, p):
        # assert sum(p) == 1
        self._p = p

    def imitate(self):
        x = random()
        k = 0
        while x > sum(self._p[:k]):
            k += 1
        return k - 1


class PiratesProblem(object):

    __pirates_count = 6
    __initial_p = 1.0 / __pirates_count
    __initial_bet = 1
    __needed_sum = 10000
    __max_rounds = 100000
    __iterations = 1000

    def solve(self):
        for p in arange(0, 1, 0.001):
            ps = [self.__initial_p + p] + [self.__initial_p - p] + [self.__initial_p] * 4
            event = CompleteGroupRandomEvent(ps)
            current_sum = 0
            for i in xrange(self.__max_rounds):
                current_sum += (self.__initial_bet * self.__pirates_count) * (event.imitate() == 0) - 1
            print "{:5.3} {:5}".format(p, current_sum)
            if current_sum > self.__needed_sum:
                return p


if __name__ == '__main__':
    print PiratesProblem().solve()