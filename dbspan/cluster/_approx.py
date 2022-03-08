import random

import networkx as nx
import numpy as np


class EdgeSelectorBlindRandom:

    def __init__(self):
        self.rng = random.Random()

    def _above(self, lower, upper, i, j, eps):
        if (i == j):
            return False
        if (lower[i][j] == 0.0):
            return True
        return upper[i][j] / lower[i][j] > 1 + eps

    def select(self, lower, upper, eps):
        n = len(lower)
        start_i = self.rng.randint(0, n - 1)
        start_j = self.rng.randint(0, n - 1)

        for i in range(n + 1):
            for j in range(n):
                x = (i + start_i) % n
                y = (j + start_j) % n
                if self._above(lower, upper, x, y, eps):
                    return x, y, False
        return -1, -1, True


class ApproxMetric:
    def __init__(self, spanner):
        self.spanner = spanner

    def __call__(self, p_idx, q_idx):
        return nx.shortest_path_length(
            self.spanner,
            p_idx,
            q_idx,
            weight='weight',
        )


class KN20Approximator:
    def __init__(self, metric, edge_selector=EdgeSelectorBlindRandom()):
        self._metric = metric
        self._selector = edge_selector

    def approximate(self, data, eps):
        graph, lower, upper = self._init(data)
        spanner = self._compute_spanner(data, eps, graph, lower, upper)
        return ApproxMetric(spanner)

    def _init(self, data):
        n = len(data)

        lower = np.zeros((n, n))

        upper = np.inf * np.ones((n, n))
        for i in range(0, n):
            upper[i][i] = 0.0

        graph = nx.empty_graph(n)
        return graph, lower, upper

    def _compute_spanner(self, data, eps, graph, lower, upper):
        i, j, done = self._selector.select(lower, upper, eps)
        while not done:
            dist = self._metric(data[i], data[j])
            graph.add_edge(i, j, weight=dist)
            self._update_bounds(lower, upper, dist, i, j)

            i, j, done = self._selector.select(lower, upper, eps)
        return graph

    def _update_bounds(self, lower, upper, dist, i, j):
        lower[i][j] = dist
        lower[j][i] = dist
        upper[i][j] = dist
        upper[j][i] = dist

        n = lower.shape[0]
        for k in range(n):
            for l in range(k + 1, n):   # noqa: E741 using notation from KN20
                ub = min(
                    upper[k][l],
                    upper[k][i] + dist + upper[j][l],
                    upper[k][j] + dist + upper[i][l],
                )

                lb = max(
                    lower[k][l],
                    dist - upper[k][i] - upper[l][j],
                    dist - upper[k][j] - upper[l][i],
                    lower[j][l] - dist - upper[k][i],
                    lower[i][l] - dist - upper[k][j],
                    lower[j][k] - dist - upper[l][i],
                    lower[i][k] - dist - upper[l][j],
                )

                upper[k][l] = ub
                lower[k][l] = lb
                upper[l][k] = ub
                lower[l][k] = lb
