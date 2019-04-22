# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from matplotlib import pyplot as plot
from random_events import (
    SimpleRandomEvent,
    ComplexRandomEvent,
    ComplexDependentRandomEvent,
    CompleteGroupRandomEvent,
)


class RandomEventTest(object):

    def test_uniformity(self):
        raise NotImplementedError

    def test_independence(self):
        raise NotImplementedError


class SimpleEventTest(RandomEventTest):

    __p = 0.33
    __iterations = [
        10,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000
    ]

    def test_uniformity(self):
        event = SimpleRandomEvent(self.__p)
        msg = 'Эксперементальная вероятность (P(A) -> {})'
        print msg.format(self.__p)
        for n in self.__iterations:
            p = sum(1.0 / n for i in xrange(n) if event.imitate())
            print "n = {:6}: P(A) = {}".format(n, p)


class ComplexEventTest(RandomEventTest):

    __pa = 0.33
    __pb = 0.46
    __iterations = [
        10,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000
    ]

    def test_uniformity(self):
        event = ComplexRandomEvent(self.__pa, self.__pb)
        msg = 'Эксперементальная вероятность (P(A) -> {}, P(B) -> {})'
        print msg.format(self.__pa, self.__pb)
        for n in self.__iterations:
            pa = 0
            pb = 0
            for i in xrange(n):
                a, b = event.imitate()
                pa += float(a) / n
                pb += float(b) / n
            msg = "n = {:6}: P(A) = {:5.3}, P(B) = {:5.3}"
            print msg.format(n, pa, pb)


class ComplexDependentEventTest(RandomEventTest):

    __pa = 0.31
    __pb = 0.54
    __pba = 0.89
    __iterations = [
        10,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000
    ]

    def test_uniformity(self):
        msg = 'Эксперементальная вероятность (P(A) -> {}, P(B) -> {}, P(B/A) -> {})'
        print msg.format(self.__pa, self.__pb, self.__pba)
        event = ComplexDependentRandomEvent(self.__pa, self.__pb, self.__pba)
        for n in self.__iterations:
            pa = 0
            pb = 0
            pba = 0
            for i in xrange(n):
                a, b = event.imitate()
                pa += float(a) / n
                pb += float(b) / n
                pba += float(a and b) / n
            msg = "n = {:6}: P(A) = {:5.3}, P(B) = {:5.3}, P(B/A) = {:5.3}"
            print msg.format(n, pa, pb, pba / pa)


class CompleteGroupEventTest(RandomEventTest):

    __p = [0.3, 0.2, 0.4, 0.1]
    __iterations = [
        10,
        50,
        100,
        500,
        1000,
        5000,
        10000,
        50000,
        100000
    ]

    def test_uniformity(self):
        event = CompleteGroupRandomEvent(self.__p)
        for n in self.__iterations:
            p = [event.imitate() for _ in xrange(n)]
            plot.hist(p, len(self.__p), weights=[1.0 / n for i in xrange(n)])
            plot.show()


if __name__ == '__main__':
    SimpleEventTest().test_uniformity()
    ComplexEventTest().test_uniformity()
    ComplexDependentEventTest().test_uniformity()
    CompleteGroupEventTest().test_uniformity()