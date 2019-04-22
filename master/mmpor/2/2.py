# -*- coding: utf-8 -*-
import numpy as np

from appointing import Appointer


if __name__ == '__main__':
    inf = -float('inf')
    a = np.array([
        [1, 8, 4, 1],
        [5, 7, 6, 5],
        [3, 5, 4, 2],
        [3, 1, 6, 3],
    ])
    a_extra = -(a - np.max(a))

    appointer = Appointer(a_extra)
    result = appointer.appoint()

    a_extra = np.zeros((a_extra.shape[0], a_extra.shape[0]))
    for i, j in result:
        a_extra[i, j] = 1

    print("Назначения:")
    print("\n".join(" ".join(str(int(e)) for e in row) for row in a_extra))
    print()

    cost = sum(a[i][j] for i, j in result)
    print("Максимальный доход:", cost)