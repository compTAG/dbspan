import random


from ..context import dbspan


def ascii_diff(p, q):
    return abs(ord(p) - ord(q))


def test_dbscan_and_dbspan():
    data = ['a', 'b', 'd', 'k', 'u', 'v', 'w']
    algo = dbspan.cluster.DBSCAN(eps=2, min_samples=2, metric=ascii_diff)
    labels = algo.fit(data)

    assert labels[0] == 1
    assert labels[1] == 1
    assert labels[2] == 1
    assert labels[3] == dbspan.cluster.NOISE
    assert labels[4] == 2
    assert labels[5] == 2
    assert labels[6] == 2

    algo = dbspan.cluster.DBSpan(
        eps=2,
        min_samples=2,
        metric=ascii_diff,
        delta=.1,
    )
    labels, dbg_data = algo.fit(data, dbg=True)
    assert labels[0] == 1
    assert labels[1] == 1
    assert labels[2] == 1
    assert labels[3] == dbspan.cluster.NOISE
    assert labels[4] == 2
    assert labels[5] == 2
    assert labels[6] == 2

    assert 'neighborhood' in dbg_data


def test_dbscan_and_dbspan_with_dgm():
    data_factory = dbspan.topology.PointSetDataFactory(seed=72330)
    dgm_factory = dbspan.topology.DiagramFactory()

    rng = random.Random(43081)

    def make_sphere_dgm():
        noise = rng.random() / 10
        points = data_factory.make_sphere(dim=4, num_points=100, noise=noise)
        return dgm_factory.make_from_point_set(points)

    def make_torus_dgm():
        noise = rng.random() / 10
        points = data_factory.make_torus(dim=4, num_points=100, noise=noise)
        return dgm_factory.make_from_point_set(points)

    def make_swiss_roll_dgm():
        noise = rng.random() / 10
        points = data_factory.make_swiss_roll(
            dim=4,
            num_points=100,
            noise=noise,
        )
        return dgm_factory.make_from_point_set(points)

    dgms = [make_sphere_dgm() for _ in range(5)] \
        + [make_torus_dgm() for _ in range(5)] \
        + [make_swiss_roll_dgm() for _ in range(1)]

    dgm_metric = dbspan.topology.DiagramMetric()

    def dgm1_metric(dgm1, dgm2):
        return dgm_metric.bottleneck(dgm1[1], dgm2[1])

    algo = dbspan.cluster.DBSCAN(metric=dgm1_metric, eps=.3, min_samples=3)
    labels = algo.fit(dgms)
    assert labels[0] == 1
    assert labels[1] == 1
    assert labels[2] == 1
    assert labels[3] == 1
    assert labels[4] == 1
    assert labels[5] == 2
    assert labels[6] == 2
    assert labels[7] == 2
    assert labels[8] == 2
    assert labels[9] == 2
    assert labels[10] == dbspan.cluster.NOISE

    algo = dbspan.cluster.DBSpan(
        metric=dgm1_metric,
        eps=.3,
        min_samples=3,
        delta=.1,
    )
    labels = algo.fit(dgms)
    assert labels[0] == 1
    assert labels[1] == 1
    assert labels[2] == 1
    assert labels[3] == 1
    assert labels[4] == 1
    assert labels[5] == 2
    assert labels[6] == 2
    assert labels[7] == 2
    assert labels[8] == 2
    assert labels[9] == 2
    assert labels[10] == dbspan.cluster.NOISE
