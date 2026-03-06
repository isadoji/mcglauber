from __future__ import annotations
import numpy as np

def pairwise_transverse_distances(a_xy: np.ndarray, b_xy: np.ndarray) -> np.ndarray:
    dx = a_xy[:, None, 0] - b_xy[None, :, 0]
    dy = a_xy[:, None, 1] - b_xy[None, :, 1]
    return np.sqrt(dx * dx + dy * dy)
