from ..context import dbspan


def test_getting_started():
    data_factory = dbspan.topology.PointSetDataFactory(seed=72330)
    dgm_factory = dbspan.topology.DiagramFactory()
    dgm_metric = dbspan.topology.DiagramMetric()

    def make_sphere(noise):
        return data_factory.make_sphere(dim=4, num_points=100, noise=noise)

    def make_torus(noise):
        return data_factory.make_torus(dim=4, num_points=100, noise=noise)

    data = {
        'sphere_clean': make_sphere(noise=0.0),
        'sphere_noisy': make_sphere(noise=0.1),
        'torus_clean': make_torus(noise=0.0),
        'torus_noisy': make_torus(noise=0.1),
    }

    dgm = {}
    for k,v in data.items():
        dgm[k] = dgm_factory.make_from_point_set(v)[1]

    expected_dists = {
        "sphere_clean:sphere_clean":0.0,
        "sphere_clean:sphere_noisy":0.08189773559570312,
        "sphere_clean:torus_clean": 0.4361886978149414,
        "sphere_clean:torus_noisy": 0.45923399925231934,
        "sphere_noisy:sphere_clean":0.08189773559570312,
        "sphere_noisy:sphere_noisy":0.0,
        "sphere_noisy:torus_clean": 0.4361886978149414,
        "sphere_noisy:torus_noisy": 0.45923399925231934,
        "torus_clean:sphere_clean": 0.4361886978149414,
        "torus_clean:sphere_noisy": 0.4361886978149414,
        "torus_clean:torus_clean": 0.0,
        "torus_clean:torus_noisy": 0.15520060062408447,
        "torus_noisy:sphere_clean": 0.45923399925231934,
        "torus_noisy:sphere_noisy": 0.45923399925231934,
        "torus_noisy:torus_clean": 0.15520060062408447,
        "torus_noisy:torus_noisy": 0.0,
    }

    for k1 in dgm.keys():
        for k2 in dgm.keys():
            dist = dgm_metric.bottleneck(dgm[k1], dgm[k2])
            assert expected_dists[k1+":"+k2] - dist < .00001

