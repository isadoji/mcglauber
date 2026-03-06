import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gzip
import json

# ================================
# 1. Grafica b vs Npart
# ================================

df = pd.read_csv("outputs/events_summary.csv")

plt.figure(figsize=(7,6))

plt.scatter(
    df["b_fm"],
    df["n_part"],
    s=10
)

plt.xlabel("Impact parameter b [fm]")
plt.ylabel("N_part")
plt.title("MC-Glauber: b vs N_part")

plt.grid(True)

plt.tight_layout()
plt.savefig("outputs/b_vs_npart.png", dpi=150)

plt.show()

