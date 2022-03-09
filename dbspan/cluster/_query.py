import networkx as nx

from ._approx import KN20Approximator


class ExactRangeQuery:
    def __init__(self, data, eps, metric):
        self.data = data
        self.eps = eps
        self.metric = metric

    def query(self, q_idx):
        q = self.data[q_idx]
        return [i for i, p in enumerate(self.data)
                if i != q_idx and self.metric(p, q) <= self.eps]


class ApproximateRangeQuery:
    def __init__(self, data, eps, metric, spanner_eps):
        approximator = KN20Approximator(metric)
        self.approx_metric = approximator.approximate(data, spanner_eps)

        lengths = nx.all_pairs_dijkstra_path_length(
            self.approx_metric.spanner,
            cutoff=eps,
        )

        self.neighborhoods = [None] * len(data)
        for neighbors in lengths:
            src, targets = neighbors
            self.neighborhoods[src] = [k for k, v in targets.items() if v != 0]

    def query(self, q_idx):
        return self.neighborhoods[q_idx]

    @property
    def spanner(self):
        return self.approx_metric.spanner
