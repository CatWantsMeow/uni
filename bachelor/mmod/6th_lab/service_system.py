# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import expovariate, normalvariate, uniform, triangular
from functools import partial
from matplotlib import pyplot as plot


global_time = 0
global_dt = 0.01


class Task(object):

    def __init__(self):
        self.t = None
        self.received = None
        self.created = global_time


class AbstractPhase(object):

    def add_task(self, task):
        raise NotImplementedError

    def imitate(self):
        raise NotImplementedError

    def stats(self):
        raise NotImplementedError


class Phase(AbstractPhase):

    def __init__(self, channels_count, rand, queue_length, next_phase):
        self._queue_length = queue_length
        self._rand = rand
        self._next = next_phase
        self._channel = [None] * channels_count
        self._queue = []
        self.queue_lengths = []
        self.states = [[0, 0, 0] for _ in xrange(channels_count)]

    def _update_times(self):
        for i, task in enumerate(self._channel):
            if not task:
                continue
            task.t -= global_dt
            if task.t <= 0:
                added = self._next.add_task(task)
                self._channel[i] = None if added else task

    def _send_tasks(self):
        for i, task in enumerate(self._channel):
            if not task and self._queue:
                self._channel[i] = self._queue.pop(0)

    def _update_stats(self):
        self.queue_lengths.append(len(self._queue))
        for i, task in enumerate(self._channel):
            if task and task.t < 0:
                self.states[i][0] += 1
            elif task is None:
                self.states[i][1] += 1
            else:
                self.states[i][2] += 1

    def add_task(self, task):
        if len(self._queue) == self._queue_length and all(task for task in self._channel):
            return False
        task.t = self._rand()
        self._queue.append(task)
        return True

    def imitate(self):
        self._update_times()
        self._send_tasks()
        self._update_stats()

    def stats(self):
        avg_queue_l = sum(self.queue_lengths) / float(len(self.queue_lengths))
        print "Средняя длинна очереди = {}".format(avg_queue_l)

        iterations = global_time / global_dt
        msg = "Вероятности состояний:"
        for i, state in enumerate(self.states):
            blocked_p = state[0] / iterations
            free_p = state[1] / iterations
            worked_p = state[2] / iterations
            msg = "#{}: заблокирован: {:.5}, свободен = {:.5}, работатет = {:.5}"
            print msg.format(i, blocked_p, free_p, worked_p)


class Sender(AbstractPhase):

    def __init__(self, next):
        self._next = next
        self._next_task = 0
        self.rejected = []
        self.total = 0

    def add_task(self, task):
        pass

    def imitate(self):
        self._next_task -= global_dt
        if self._next_task <= 0:
            self.total += 1
            self._next_task = expovariate(1)
            task = Task()
            added = self._next.add_task(task)
            if not added:
                self.rejected.append(task)

    def stats(self):
        reject_p = len(self.rejected) / float(self.total)
        print "Вероятность оказа: {:.5}".format(reject_p)


class Receiver(AbstractPhase):

    def __init__(self):
        self.completed = []

    def add_task(self, task):
        task.received = global_time
        self.completed.append(task)
        return True

    def imitate(self):
        pass

    def stats(self):
        completed = self.completed
        intervals = []
        for i in xrange(1, len(completed)):
            intervals.append(abs(completed[i].received - completed[i - 1].received))
        plot.hist(intervals, bins=50)
        plot.show()

        e = sum(intervals) / float(len(intervals))
        d = sum(((i - e) ** 2) for i in intervals) / len(intervals)
        print "Мат. ожидание интервала между заявками: {:.5}".format(e)
        print "Дисперсия интервала между заявками: {:.5}".format(d)

        process_times = [t.received - t.created for t in completed]
        plot.hist(process_times, bins=50)
        plot.show()

        e = sum(process_times) / len(process_times)
        d = sum(((i - e) ** 2) for i in process_times) / len(process_times)
        print "Мат. ожидание времени обработки заявки: {:.5}".format(e)
        print "Дисперсия времени обработки заявки: {:.5}".format(d)


class ServiceSystem(object):

    __receiver = Receiver()
    __phase_5 = Phase(5, partial(triangular, 2, 5, 3.5), 3, __receiver)
    __phase_4 = Phase(3, partial(uniform, 3, 9), 3, __phase_5)
    __phase_3 = Phase(4, partial(normalvariate, 5, 1), 3, __phase_4)
    __phase_2 = Phase(4, partial(normalvariate, 5, 2), 0, __phase_3)
    __phase_1 = Phase(3, partial(uniform, 3, 9), 3, __phase_2)
    __source = Sender(__phase_1)

    __phases = [
        __source,
        __phase_1,
        __phase_2,
        __phase_3,
        __phase_4,
        __phase_5,
        __receiver
    ]

    def __init__(self, rounds=10000):
        self._rounds = rounds

    def imitate(self):
        for phase in self.__phases:
            phase.imitate()

    def start(self):
        global global_time
        global_time = 0
        while len(self.__receiver.completed) < self._rounds:
            self.imitate()
            global_time += global_dt

    def stats(self):
        for i, phase in enumerate(self.__phases):
            print "Фаза #{}".format(i)
            phase.stats()
            print


if __name__ == '__main__':
    system = ServiceSystem(1000)
    system.start()
    system.stats()
