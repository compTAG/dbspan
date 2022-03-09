from ._query import ExactRangeQuery, ApproximateRangeQuery


NOISE = 0


class _XXScan:
    def _is_labeled(self, label):
        return label > NOISE

    def _make_range_query(self, data):
        return self.range_query_algo(data, self.eps, self.metric)

    def __init__(self, metric, range_query_algo, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.range_query_algo = range_query_algo

    def fit(self, data):
        cur_label = NOISE
        labels = [NOISE - 1] * len(data)
        neighborhood = self._make_range_query(data)

        for p_idx, p in enumerate(data):
            if self._is_labeled(labels[p_idx]):
                continue

            p_neighbors = neighborhood.query(p_idx)
            if len(p_neighbors) < self.min_samples:
                labels[p_idx] = NOISE
                continue

            cur_label += 1
            labels[p_idx] = cur_label
            queue = p_neighbors

            while queue:
                q_idx = queue.pop(0)

                q_label = labels[q_idx]
                if self._is_labeled(q_label):
                    continue

                labels[q_idx] = cur_label
                q_neighbors = neighborhood.query(q_idx)
                if len(q_neighbors) >= self.min_samples:
                    queue = queue + q_neighbors

        return labels


class DBSCAN(_XXScan):
    def __init__(self, metric, eps=.5, min_samples=5):
        super().__init__(metric, ExactRangeQuery, eps, min_samples)


class DBSpan(_XXScan):
    def __init__(self, metric, eps=.5, min_samples=5):
        super().__init__(metric, ApproximateRangeQuery, eps, min_samples)
