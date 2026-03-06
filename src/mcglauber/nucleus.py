from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np
from .sampling import woods_saxon_density

@dataclass
class Nucleus:
    name: str
    A: int
    radius_fm: float
    diffuseness_fm: float
    min_distance_fm: float

    def sample_nucleons(self, rng: np.random.Generator) -> np.ndarray:
        positions: list[np.ndarray] = []
        r_max = self.radius_fm + 10.0 * self.diffuseness_fm
        while len(positions) < self.A:
            x = rng.uniform(-r_max, r_max)
            y = rng.uniform(-r_max, r_max)
            z = rng.uniform(-r_max, r_max)
            r = math.sqrt(x * x + y * y + z * z)
            if r > r_max:
                continue
            accept_prob = woods_saxon_density(r=r, radius_fm=self.radius_fm, diffuseness_fm=self.diffuseness_fm)
            if rng.uniform(0.0, 1.0) > accept_prob:
                continue
            candidate = np.array([x, y, z], dtype=float)
            if positions:
                prev = np.vstack(positions)
                distances = np.linalg.norm(prev - candidate, axis=1)
                if np.any(distances < self.min_distance_fm):
                    continue
            positions.append(candidate)
        return np.vstack(positions)
