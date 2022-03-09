import abc


from ._query import ExactRangeQuery, ApproximateRangeQuery


NOISE = 0


class _XXScan(abc.ABC):

    @abc.abstractmethod
    def _make_range_query(self, data, eps, metric):
        pass

    def _is_labeled(self, label):
        return label > NOISE

    def __init__(self, metric, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric

    def fit(self, data, dbg=False):
        '''
        Run a density based clustering algorithm on the data.

        Note that the interface takes a keyword argument of 'dbg'.  uSE
        THE 'dbg' ARGUMENT WITH CAUTION!!!  It is NOT intended
        general use (and is really just for access the internals of the
        algorithm for the experimental section of a paper.

        Keyword arguments:
        data -- the data to use for the clustering
        '''
        cur_label = NOISE
        labels = [NOISE - 1] * len(data)
        neighborhood = self._make_range_query(data, self.eps, self.metric)

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

        if not dbg:
            return labels

        else:
            return labels, {
                'neighborhood': neighborhood,
            }



class DBSCAN(_XXScan):
    def _make_range_query(self, data, eps, metric):
        return ExactRangeQuery(data, eps, metric)


class DBSpan(_XXScan):
    def _make_range_query(self, data, eps, metric):
        return ApproximateRangeQuery(data, eps, metric, self.delta)

    def __init__(self, metric, eps, min_samples, delta):
        super().__init__(metric, eps, min_samples)
        self.delta = delta
