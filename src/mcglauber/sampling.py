from __future__ import annotations
import math
import numpy as np

def sample_impact_parameter(rng: np.random.Generator, b_max_fm: float) -> float:
    u = rng.uniform(0.0, 1.0)
    return b_max_fm * math.sqrt(u)

def woods_saxon_density(r: float, radius_fm: float, diffuseness_fm: float) -> float:
    return 1.0 / (1.0 + math.exp((r - radius_fm) / diffuseness_fm))
