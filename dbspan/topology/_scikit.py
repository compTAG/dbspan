import random

import numpy as np
import persim
import ripser
import tadasets


class PointSetDataFactory:

    def _seed_numpy_rng_hack(self):
        # Note that I have no idea why, but the version of TaDAsets that is
        # availbled on pip does not match the version documented.  So,
        # to seed, I seed the numpy global generator, which is what theircode
        # does.
        maxint = 2**32 - 1
        minint = 0
        seed = self.rng.randint(minint, maxint)
        np.random.seed(seed)

    def __init__(self, seed=None):
        self.rng = random.Random()
        if seed:
            self.rng.seed(seed)

    def make_sphere(self, dim, num_points, noise):
        self._seed_numpy_rng_hack()
        return tadasets.dsphere(d=dim, n=num_points, noise=noise)

    def make_torus(self, dim, num_points, noise):
        self._seed_numpy_rng_hack()
        return tadasets.torus(ambient=dim, n=num_points, noise=noise)

    def make_swiss_roll(self, dim, num_points, noise):
        self._seed_numpy_rng_hack()
        return tadasets.swiss_roll(ambient=dim, n=num_points, noise=noise)


class Diagram:
    def __init__(self, dgms):
        self.dgms = dgms

    def __getitem__(self, item):
        return self.dgms[item]


class DiagramFactory:

    def make_from_point_set(self, pointset):
        return Diagram(ripser.ripser(pointset)['dgms'])


class DiagramMetric:

    def bottleneck(self, dgm1, dgm2):
        return persim.bottleneck(dgm1, dgm2)
