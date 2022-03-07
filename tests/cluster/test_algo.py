import random

from ..context import dbspan


def test_dbscan():
    data = [1, 2, 4, 10, 20, 21, 22]

    algo = dbspan.cluster.DBScan(eps=2, min_samples=2)
    labels = algo.fit(data)

    noise = algo.__class__.noise()

    assert labels[1] == 0
    assert labels[2] == 0
    assert labels[4] == 0
    assert labels[10] == noise
    assert labels[20] == 1
    assert labels[21] == 1
    assert labels[22] == 1


def test_dbscan_with_dgm():
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

    algo = dbspan.cluster.DBScan(eps=.3, min_samples=3, metric=dgm1_metric)
    labels = algo.fit(dgms)

    assert labels[dgms[0]] == 0
    assert labels[dgms[1]] == 0
    assert labels[dgms[2]] == 0
    assert labels[dgms[3]] == 0
    assert labels[dgms[4]] == 0
    assert labels[dgms[5]] == 1
    assert labels[dgms[6]] == 1
    assert labels[dgms[7]] == 1
    assert labels[dgms[8]] == 1
    assert labels[dgms[9]] == 1
    assert labels[dgms[10]] == -1
