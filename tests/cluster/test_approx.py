from ..context import dbspan

import networkx as nx


def test_approx_init():
    def metric(x, y):
        return abs(ord(x) - ord(y))

    approximator = dbspan.cluster.Approximator(metric)

    n = 10
    eps = 3
    data = [chr(ord('a')+i) for i in range(n)]
    approx_metric = approximator.approximate(data, eps)

    for p_idx, p in enumerate(data):
        for q_idx in range(p_idx+1, n):
            q = data[q_idx]
            exact_dist = metric(p, q)
            approx_dist = approx_metric(p_idx, q_idx)
            assert approx_dist <= (1 + eps) * exact_dist

