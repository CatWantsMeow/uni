# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.datasets.samples_generator import make_blobs


# генерация данных
def generate_data(k):
    centers = [[2, 2], [-2, -2], [-2, 2]]
    x, _ = make_blobs(n_samples=k, centers=centers, cluster_std=2)
    return x, len(centers)


# функция поиска кластеров
def find_clusters(x, n):
    # поиск кластеров
    k_means = KMeans(n_clusters=n, n_init=100)
    k_means.fit(x)

    # определение элементов, попавших в каждый кластер
    k_means_centers = np.sort(k_means.cluster_centers_, axis=0)
    k_means_indexes = pairwise_distances_argmin(x, k_means_centers)
    return k_means_centers, k_means_indexes


def main():
    # генерация исходных данных и поиск кластеров
    x, n = generate_data(3000)
    centers, indices = find_clusters(x, n)

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    # график исходных данных
    ax1.plot(
        x[:, 0], x[:, 1], 'w',
        markerfacecolor='black', marker='.', label='Members'
    )

    # график кластеров
    colors = ['green', 'blue', 'red']
    markers = ['.', 'X', '^']
    for k in range(n):
        members = indices == k
        ax2.plot(
            x[members, 0], x[members, 1], 'w',
            markerfacecolor=colors[k],
            marker=markers[k],
            label='{}th cluster'.format(k + 1)
        )

    ax2.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    main()
