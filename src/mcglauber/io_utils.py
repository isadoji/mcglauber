from __future__ import annotations
from pathlib import Path
import gzip
import json
import pandas as pd
import matplotlib.pyplot as plt

def ensure_dir(path: str | Path) -> Path:
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out

def save_dataframe(df: pd.DataFrame, path: str | Path) -> None:
    df.to_csv(path, index=False)

def save_histogram(series, xlabel: str, path: str | Path, bins: int = 50) -> None:
    plt.figure(figsize=(7, 5))
    plt.hist(series, bins=bins)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

def save_event_geometries_jsonl(records: list[dict], path: str | Path) -> None:
    path = Path(path)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec))
            f.write("\n")
