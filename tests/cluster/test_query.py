import pytest

from ..context import dbspan


def ascii_diff(p, q):
    return abs(ord(p) - ord(q))


def test_exact_range_query():
    data = ['a', 'b', 'c', 'h']

    rq = dbspan.cluster.ExactRangeQuery(data, eps=2, metric=ascii_diff)
    with pytest.raises(IndexError):
        assert rq.query(6) == []
    assert rq.query(0) == [1, 2]
    assert rq.query(1) == [0, 2]
    assert rq.query(2) == [0, 1]
    assert rq.query(3) == []


def test_approx_range_query():
    data = ['a', 'b', 'c', 'h']

    rq = dbspan.cluster.ApproximateRangeQuery(
        data,
        eps=2,
        metric=ascii_diff,
        spanner_eps=.1,
    )
    assert set(rq.query(0)) == {1, 2}
    assert set(rq.query(1)) == {0, 2}
    assert set(rq.query(2)) == {0, 1}
    assert rq.query(3) == []
