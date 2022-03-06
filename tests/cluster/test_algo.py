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
