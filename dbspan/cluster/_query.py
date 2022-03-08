class ExactRangeQuery:
    def __init__(self, data, eps, metric):
        self.data = data
        self.eps = eps
        self.metric = metric

    def query(self, q_idx):
        q = self.data[q_idx]
        return [i for i, p in enumerate(self.data)
                if i != q_idx and self.metric(p, q) <= self.eps]


    def query(self, q):
        return [p for p in self.data
                if p != q and self.metric(p, q) <= self.eps]
