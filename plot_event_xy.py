import gzip
import json
import numpy as np
import matplotlib.pyplot as plt
import random


event_id = random.randint(0, 100)   # evento que quieres visualizar


# ================================
# Leer evento
# ================================

with gzip.open("outputs/event_geometries.jsonl.gz","rt") as f:

    for line in f:
        event = json.loads(line)

        if event["event_id"] == event_id:
            break


# ================================
# Datos del evento
# ================================

x_proj = np.array(event["projectile_x_fm"])
y_proj = np.array(event["projectile_y_fm"])

x_targ = np.array(event["target_x_fm"])
y_targ = np.array(event["target_y_fm"])

mask_proj = np.array(event["projectile_participant_mask"])
mask_targ = np.array(event["target_participant_mask"])

b = event["b_fm"]
npart = event["n_part"]
ncoll = event["n_coll"]


# ================================
# Grafica
# ================================

plt.figure(figsize=(7,7))

# espectadores
plt.scatter(
    x_proj[mask_proj==0],
    y_proj[mask_proj==0],
    s=10,
    label="Projectile spectators"
)

plt.scatter(
    x_targ[mask_targ==0],
    y_targ[mask_targ==0],
    s=10,
    label="Target spectators"
)

# participantes
plt.scatter(
    x_proj[mask_proj==1],
    y_proj[mask_proj==1],
    s=30,
    label="Projectile participants"
)

plt.scatter(
    x_targ[mask_targ==1],
    y_targ[mask_targ==1],
    s=30,
    label="Target participants"
)


plt.xlabel("x [fm]")
plt.ylabel("y [fm]")
plt.axis("equal")

plt.title(f"Glauber Event {event_id}")


# ================================
# Texto con parámetros físicos
# ================================

textstr = (
    f"b = {b:.2f} fm\n"
    f"Npart = {npart}\n"
    f"Ncoll = {ncoll}"
)

plt.text(
    0.02,
    0.98,
    textstr,
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment='top',
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)


plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(f"outputs/event_{event_id}_geometry.png", dpi=150)

plt.show()