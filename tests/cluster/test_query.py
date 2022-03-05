from ..context import dbspan


def one_norm(p, q):
    return abs(p - q)


def test_exact_range_query():
    data = [1, 2, 3]

    rq = dbspan.cluster.ExactRangeQuery(data, eps=2, metric=one_norm)
    assert rq.query(-2) == set()
    assert rq.query(-1) == {1}
    assert rq.query(0) == { 1, 2 }
    assert rq.query(1) == { 1, 2, 3 }
    assert rq.query(2) == { 1, 2, 3 }
    assert rq.query(3) == { 1, 2, 3 }
    assert rq.query(4) == { 2, 3 }
    assert rq.query(5) == { 3 }
    assert rq.query(6) == set()
