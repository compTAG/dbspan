import numpy as np
import sklearn.cluster

from ._query import ApproximateRangeQuery


NOISE = 0


class DBSCAN:
    def __init__(self, metric, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric

    def _pairwise_distance_matrix(self, data):
        n = len(data)
        dist_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(i + 1, n):
                dist = self.metric(data[i], data[j])
                dist_matrix[i][j] = dist
                dist_matrix[j][i] = dist

        return dist_matrix

    def fit(self, data):
        dist_matrix = self._pairwise_distance_matrix(data)

        clustering = sklearn.cluster.DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples,
            metric='precomputed',
        )
        clustering.fit(dist_matrix)

        # scikit learn uses -1 for noise, to be consistent between the
        # implementation and the code we add 1 to the scikit learn labels
        # so that 0 is noise and cluster labels are positive.
        return clustering.labels_ + 1


class DBSpan:
    def _is_labeled(self, label):
        return label > NOISE

    def __init__(self, metric, eps, min_samples, delta):
        self.eps = eps
        self.min_samples = min_samples
        self.metric = metric
        self.delta = delta

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
        neighborhood = ApproximateRangeQuery(
            data,
            self.eps,
            self.metric,
            self.delta,
        )

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
