from __future__ import annotations
import math
from pathlib import Path
import numpy as np
import pandas as pd

def mb_to_fm2(sigma_mb: float) -> float:
    return 0.1 * sigma_mb

def collision_radius_fm(sigma_inel_nn_mb: float) -> float:
    sigma_fm2 = mb_to_fm2(sigma_inel_nn_mb)
    return math.sqrt(sigma_fm2 / math.pi)

def load_sigma_table(csv_path: str | Path) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"No existe la tabla: {path}")
    df = pd.read_csv(path)
    required = {"sqrts_gev", "sigma_inel_nn_mb"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {path}: {missing}. Columnas requeridas: {required}")
    df = df[["sqrts_gev", "sigma_inel_nn_mb"]].dropna().copy()
    df = df.sort_values("sqrts_gev").reset_index(drop=True)
    if len(df) < 2:
        raise ValueError("La tabla debe tener al menos dos puntos para interpolar.")
    if not np.all(np.diff(df["sqrts_gev"].to_numpy(dtype=float)) > 0):
        raise ValueError("La columna sqrts_gev debe ser estrictamente creciente.")
    return df

def interpolate_sigma_inel_nn(sqrts_gev: float, csv_path: str | Path, interpolation_space: str = "log_sqrt_s") -> float:
    df = load_sigma_table(csv_path)
    x = df["sqrts_gev"].to_numpy(dtype=float)
    y = df["sigma_inel_nn_mb"].to_numpy(dtype=float)
    xmin = float(np.min(x))
    xmax = float(np.max(x))
    if sqrts_gev < xmin or sqrts_gev > xmax:
        raise ValueError(f"La energía sqrt(s_NN)={sqrts_gev} GeV está fuera del rango de interpolación [{xmin}, {xmax}] GeV.")
    if interpolation_space == "linear":
        return float(np.interp(float(sqrts_gev), x, y))
    if interpolation_space == "log_sqrt_s":
        return float(np.interp(np.log(float(sqrts_gev)), np.log(x), y))
    raise ValueError(f"interpolation_space desconocido: {interpolation_space}")

def resolve_sigma_inel_nn_mb(sqrts_gev: float, sigma_mode: str, sigma_inel_nn_mb: float | None = None, sigma_table_csv: str | None = None, interpolation_space: str = "log_sqrt_s") -> float:
    if sigma_mode == "fixed":
        if sigma_inel_nn_mb is None:
            raise ValueError("sigma_inel_nn_mb no puede ser None en modo 'fixed'.")
        return float(sigma_inel_nn_mb)
    if sigma_mode == "interpolate":
        if sigma_table_csv is None:
            raise ValueError("sigma_table_csv no puede ser None en modo 'interpolate'.")
        return interpolate_sigma_inel_nn(sqrts_gev=sqrts_gev, csv_path=sigma_table_csv, interpolation_space=interpolation_space)
    raise ValueError(f"Modo desconocido: {sigma_mode}")
