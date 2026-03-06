from __future__ import annotations
import pandas as pd

def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "n_events": [len(df)],
        "mean_b_fm": [df["b_fm"].mean()],
        "mean_n_part": [df["n_part"].mean()],
        "mean_n_coll": [df["n_coll"].mean()],
        "max_n_part": [df["n_part"].max()],
        "max_n_coll": [df["n_coll"].max()],
        "sigma_inel_nn_mb": [df["sigma_inel_nn_mb"].iloc[0]],
        "sqrts_gev": [df["sqrts_gev"].iloc[0]],
    })
