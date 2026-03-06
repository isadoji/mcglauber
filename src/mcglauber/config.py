from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import yaml

@dataclass
class NucleusConfig:
    name: str
    A: int
    radius_fm: float
    diffuseness_fm: float
    min_distance_fm: float

@dataclass
class BeamConfig:
    sqrts_gev: float
    sigma_mode: str = "fixed"
    sigma_inel_nn_mb: float | None = None
    sigma_table_csv: str | None = None
    interpolation_space: str = "log_sqrt_s"

@dataclass
class SimulationConfig:
    n_events: int
    b_max_fm: float
    seed: int

@dataclass
class OutputConfig:
    outdir: str
    save_summary_csv: bool
    save_histograms: bool
    save_event_geometries: bool
    event_geometry_format: str = "jsonl"

@dataclass
class FullConfig:
    projectile: NucleusConfig
    target: NucleusConfig
    beam: BeamConfig
    simulation: SimulationConfig
    output: OutputConfig

def _load_yaml(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_config(path: str | Path) -> FullConfig:
    raw = _load_yaml(path)
    projectile = NucleusConfig(**raw["system"]["projectile"])
    target = NucleusConfig(**raw["system"]["target"])
    beam = BeamConfig(**raw["beam"])
    simulation = SimulationConfig(**raw["simulation"])
    output = OutputConfig(**raw["output"])
    _validate_config(beam, output)
    return FullConfig(
        projectile=projectile,
        target=target,
        beam=beam,
        simulation=simulation,
        output=output,
    )

def _validate_config(beam: BeamConfig, output: OutputConfig) -> None:
    valid_sigma_modes = {"fixed", "interpolate"}
    if beam.sigma_mode not in valid_sigma_modes:
        raise ValueError(f"sigma_mode='{beam.sigma_mode}' no es válido. Usa uno de {valid_sigma_modes}.")
    if beam.sigma_mode == "fixed" and beam.sigma_inel_nn_mb is None:
        raise ValueError("Cuando sigma_mode='fixed' debes definir sigma_inel_nn_mb.")
    if beam.sigma_mode == "interpolate" and beam.sigma_table_csv is None:
        raise ValueError("Cuando sigma_mode='interpolate' debes definir sigma_table_csv.")
    valid_interp = {"linear", "log_sqrt_s"}
    if beam.interpolation_space not in valid_interp:
        raise ValueError(f"interpolation_space='{beam.interpolation_space}' no es válido. Usa uno de {valid_interp}.")
    valid_formats = {"jsonl"}
    if output.event_geometry_format not in valid_formats:
        raise ValueError(f"event_geometry_format='{output.event_geometry_format}' no es válido. Usa uno de {valid_formats}.")
