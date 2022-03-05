class ExactRangeQuery:
    def __init__(self, data, eps, metric):
        self.data = data
        self.eps = eps
        self.metric = metric

    def query(self, q):
        return {p for p in self.data if self.metric(p, q) <= self.eps}
