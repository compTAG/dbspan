from ..context import dbspan

import networkx as nx


def test_approx_init():
    def metric(x, y):
        return abs(x - y)

    approximator = dbspan.cluster.Approximator(metric)

    eps = .5
    data = range(10)
    spanner = approximator.approximate(data, eps)

    for i in data:
        for j in range(i + 1, len(data)):
            exact_dist = metric(i, j)
            approx_dist = nx.shortest_path_length(spanner, i, j)
            assert approx_dist <= (1 + eps) * exact_dist
