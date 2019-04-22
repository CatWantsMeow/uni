import numpy as np

from branches import BranchesMethod


def solve(c, a, b, d_low, d_high):
    method = BranchesMethod(c, a, b, list(zip(d_low, d_high)))
    ans = method.solve()
    if ans is not None:
        print("Количество служащих: ", ans[:a.shape[0]])
        print("Затрвты:", np.dot(-c, ans))


def part_a():
    c = np.array([8, 8, 6, 7, 9, 10, 8, 6, 6])
    t = np.array([8, 8, 4, 4, 4, 4, 4, 4, 4])
    b = np.array([16, 30, 31, 45, 66, 72, 61, 34, 16, 10])
    a = np.array([
        [1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 1],
    ])

    a_extra = -np.eye(a.shape[0], a.shape[0])
    a = np.hstack([a, a_extra])

    c = -c * t
    c = np.append(c, np.zeros([a.shape[0]]))

    d_low = np.array([0 for _ in range(a.shape[1])])
    d_high = np.array([np.inf for _ in range(a.shape[1])])
    solve(c, a, b, d_low, d_high)


def part_b():
    c = np.array([8, 8, 6, 7, 9, 10, 8, 6, 6])
    t = np.array([8, 8, 4, 4, 4, 4, 4, 4, 4])
    b = np.array([16, 30, 31, 45, 66, 72, 61, 34, 16, 10])
    a = np.array([
        [1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 1],
    ])

    a_extra = -np.eye(a.shape[0], a.shape[0])
    a = np.hstack([a, a_extra])

    c = -c * t
    c = np.append(c, np.zeros([a.shape[0]]))

    d_low = np.array([4, 4] + [0 for _ in range(a.shape[1] - 2)])
    d_high = np.array([np.inf for _ in range(a.shape[1])])
    solve(c, a, b, d_low, d_high)


def part_c():
    c = np.array([8, 8, 6, 7, 9, 10, 8, 6, 6])
    t = np.array([8, 8, 4, 4, 4, 4, 4, 4, 4])
    b = np.array([16, 30, 31, 45, 66, 72, 61, 34, 16, 10])
    a = np.array([
        [1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 1],
    ])

    a = np.vstack([a, np.array([1 for _ in range(a.shape[1])])])
    a_extra = -np.eye(a.shape[0], a.shape[0])
    a = np.hstack([a, a_extra])
    a[-1, -1] = 1

    b = np.hstack([b, np.array([94])])

    c = -c * t
    c = np.append(c, np.zeros([a.shape[0]]))

    d_low = np.array([4, 4] + [0 for _ in range(a.shape[1] - 2)])
    d_high = np.array([np.inf for _ in range(a.shape[1])])
    solve(c, a, b, d_low, d_high)


if __name__ == '__main__':
    print('Часть A:')
    part_a()
    print()

    print('Часть Б:')
    part_b()
    print()

    print('Часть В:')
    part_c()
    print()