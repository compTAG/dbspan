from ._query import ExactRangeQuery


class DBScan:
    @staticmethod
    def noise():
        return -1

    def _make_range_query(self, data):
        return ExactRangeQuery(data, self.eps, self.metric)

    def __init__(self, eps=.5, min_samples=5, metric=lambda p, q: abs(p - q)):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric

    def fit(self, data):
        noise = self.__class__.noise()

        cur_label = noise
        labels = [None]*len(data)
        neighborhood = self._make_range_query(data)

        for p_idx, p in enumerate(data):
            if labels[p_idx] is not None:
                continue

            p_neighbors = neighborhood.query(p_idx)
            if len(p_neighbors) < self.min_samples:
                labels[p_idx] = noise
                continue

            cur_label += 1
            labels[p_idx] = cur_label
            seeds = p_neighbors

            while seeds:
                q_idx = seeds.pop(0)

                q_label = labels[q_idx]
                if q_label is not None and q_label != noise:
                    continue

                labels[q_idx] = cur_label
                q_neighbors = neighborhood.query(q_idx)
                if len(q_neighbors) >= self.min_samples:
                    seeds = seeds + q_neighbors

        return labels
