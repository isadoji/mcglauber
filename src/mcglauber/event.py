from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from .cross_section import collision_radius_fm
from .geometry import pairwise_transverse_distances
from .sampling import sample_impact_parameter
from .nucleus import Nucleus

@dataclass
class EventResult:
    event_id: int
    b_fm: float
    n_part: int
    n_coll: int
    n_part_proj: int
    n_part_targ: int
    proj_xy: np.ndarray = field(repr=False)
    targ_xy: np.ndarray = field(repr=False)
    proj_hit: np.ndarray = field(repr=False)
    targ_hit: np.ndarray = field(repr=False)

    def summary_dict(self, sigma_inel_nn_mb: float, sqrts_gev: float) -> dict:
        return {
            "event_id": self.event_id,
            "b_fm": float(self.b_fm),
            "n_part": int(self.n_part),
            "n_coll": int(self.n_coll),
            "n_part_proj": int(self.n_part_proj),
            "n_part_targ": int(self.n_part_targ),
            "sigma_inel_nn_mb": float(sigma_inel_nn_mb),
            "sqrts_gev": float(sqrts_gev),
        }

    def geometry_dict(self, sigma_inel_nn_mb: float, sqrts_gev: float) -> dict:
        return {
            "event_id": int(self.event_id),
            "b_fm": float(self.b_fm),
            "n_part": int(self.n_part),
            "n_coll": int(self.n_coll),
            "n_part_proj": int(self.n_part_proj),
            "n_part_targ": int(self.n_part_targ),
            "sigma_inel_nn_mb": float(sigma_inel_nn_mb),
            "sqrts_gev": float(sqrts_gev),
            "projectile_x_fm": self.proj_xy[:, 0].astype(float).tolist(),
            "projectile_y_fm": self.proj_xy[:, 1].astype(float).tolist(),
            "target_x_fm": self.targ_xy[:, 0].astype(float).tolist(),
            "target_y_fm": self.targ_xy[:, 1].astype(float).tolist(),
            "projectile_participant_mask": self.proj_hit.astype(int).tolist(),
            "target_participant_mask": self.targ_hit.astype(int).tolist(),
        }

def run_event(event_id: int, rng: np.random.Generator, projectile: Nucleus, target: Nucleus, sigma_inel_nn_mb: float, b_max_fm: float) -> EventResult:
    b = sample_impact_parameter(rng, b_max_fm)
    proj_xyz = projectile.sample_nucleons(rng)
    targ_xyz = target.sample_nucleons(rng)
    proj_xyz[:, 0] -= b / 2.0
    targ_xyz[:, 0] += b / 2.0
    proj_xy = proj_xyz[:, :2].copy()
    targ_xy = targ_xyz[:, :2].copy()
    d = pairwise_transverse_distances(proj_xy, targ_xy)
    d_max = collision_radius_fm(sigma_inel_nn_mb)
    collisions = d < d_max
    proj_hit = np.any(collisions, axis=1)
    targ_hit = np.any(collisions, axis=0)
    n_part_proj = int(np.sum(proj_hit))
    n_part_targ = int(np.sum(targ_hit))
    n_part = n_part_proj + n_part_targ
    n_coll = int(np.sum(collisions))
    return EventResult(event_id=event_id, b_fm=float(b), n_part=n_part, n_coll=n_coll, n_part_proj=n_part_proj, n_part_targ=n_part_targ, proj_xy=proj_xy, targ_xy=targ_xy, proj_hit=proj_hit, targ_hit=targ_hit)
