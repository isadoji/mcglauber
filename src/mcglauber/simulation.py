from __future__ import annotations
import pandas as pd
import numpy as np
from tqdm import tqdm
from .config import FullConfig
from .nucleus import Nucleus
from .event import run_event, EventResult
from .cross_section import resolve_sigma_inel_nn_mb

def run_simulation(cfg: FullConfig) -> tuple[pd.DataFrame, list[dict], float]:
    rng = np.random.default_rng(cfg.simulation.seed)
    projectile = Nucleus(name=cfg.projectile.name, A=cfg.projectile.A, radius_fm=cfg.projectile.radius_fm, diffuseness_fm=cfg.projectile.diffuseness_fm, min_distance_fm=cfg.projectile.min_distance_fm)
    target = Nucleus(name=cfg.target.name, A=cfg.target.A, radius_fm=cfg.target.radius_fm, diffuseness_fm=cfg.target.diffuseness_fm, min_distance_fm=cfg.target.min_distance_fm)
    sigma_inel_nn_mb = resolve_sigma_inel_nn_mb(
        sqrts_gev=cfg.beam.sqrts_gev,
        sigma_mode=cfg.beam.sigma_mode,
        sigma_inel_nn_mb=cfg.beam.sigma_inel_nn_mb,
        sigma_table_csv=cfg.beam.sigma_table_csv,
        interpolation_space=cfg.beam.interpolation_space,
    )
    summary_rows: list[dict] = []
    geometry_rows: list[dict] = []
    for event_id in tqdm(range(cfg.simulation.n_events), total=cfg.simulation.n_events, desc="Simulating"):
        res: EventResult = run_event(
            event_id=event_id,
            rng=rng,
            projectile=projectile,
            target=target,
            sigma_inel_nn_mb=sigma_inel_nn_mb,
            b_max_fm=cfg.simulation.b_max_fm,
        )
        summary_rows.append(res.summary_dict(sigma_inel_nn_mb, cfg.beam.sqrts_gev))
        if cfg.output.save_event_geometries:
            geometry_rows.append(res.geometry_dict(sigma_inel_nn_mb, cfg.beam.sqrts_gev))
    return pd.DataFrame(summary_rows), geometry_rows, sigma_inel_nn_mb
