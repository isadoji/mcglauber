
# Monte Carlo Glauber Model (MCGlauber)

## Overview

This project implements a **modular Monte Carlo Glauber model in Python** for simulating the geometry of relativistic heavy‑ion collisions.

The code generates event‑by‑event nuclear collisions and computes geometrical observables commonly used in heavy‑ion physics:

- Impact parameter (b)
- Number of participants (Npart)
- Number of binary nucleon–nucleon collisions (Ncoll)
- Spatial distribution of nucleons in the transverse plane

The output can be used to analyze **initial conditions for hydrodynamics**, compute eccentricities, or study event‑by‑event geometry.

Typical applications include simulations relevant to:

- RHIC
- LHC
- NICA

---

# 1. Physical Background

## Glauber Model

The Glauber model describes a nucleus–nucleus collision as a superposition of independent nucleon–nucleon collisions.

Two nucleons collide if

d_ij < sqrt( sigma_NN_inel / pi )

where

- d_ij = transverse distance
- sigma_NN_inel = inelastic nucleon–nucleon cross section

---

## Nuclear Density Distribution

Nucleon positions follow the Woods–Saxon distribution

rho(r) = rho0 / (1 + exp((r - R)/a))

R = nuclear radius  
a = surface diffuseness

---

## Impact Parameter

The probability distribution of the impact parameter is

P(b) ∝ b

implemented as

b = b_max * sqrt(u)

where u is uniformly distributed.

---

# 2. Observables

### Number of Participants

N_part = N_part_proj + N_part_targ

### Number of Binary Collisions

N_coll = total nucleon–nucleon collisions

### Event Geometry

The transverse coordinates (x,y) define the spatial anisotropy of the collision.

---

# 3. Project Structure

mcglauber_project/

config/
default.yaml

data/
sigma_nn_inel.csv

src/mcglauber/

config.py
cross_section.py
nucleus.py
sampling.py
geometry.py
event.py
simulation.py
observables.py
io_utils.py
cli.py

outputs/

environment.yml
pyproject.toml
README.md

---

# 4. Module Description

## config.py

Reads the YAML configuration and validates parameters.

Defines:

- nuclear species
- collision energy
- cross section model
- simulation parameters

---

## cross_section.py

Handles nucleon–nucleon cross sections.

Features:

- conversion mb ↔ fm²
- collision radius calculation
- interpolation of sigma_NN_inel from experimental tables

---

## nucleus.py

Defines the Nucleus class.

Generates nucleon positions using Woods–Saxon sampling.

---

## sampling.py

Monte Carlo sampling utilities:

- impact parameter sampling
- Woods–Saxon density function

---

## geometry.py

Computes transverse distances between nucleons.

d_ij = sqrt((x_i - x_j)^2 + (y_i - y_j)^2)

---

## event.py

Simulates a single collision event:

1. sample impact parameter
2. generate nuclei
3. shift nuclei by b
4. compute nucleon distances
5. determine collisions
6. compute Npart and Ncoll

---

## simulation.py

Runs the full Monte Carlo simulation across many events.

Collects event statistics and geometry.

---

## observables.py

Computes statistical summaries such as mean Npart and Ncoll.

---

## io_utils.py

Handles:

- CSV output
- geometry files
- plots

---

## cli.py

Command‑line interface.

Run simulation using

mcglauber --config config/default.yaml

---

# 5. Output Files

## events_summary.csv

Contains one row per event:

event_id  
b_fm  
n_part  
n_coll  
n_part_proj  
n_part_targ  
sigma_inel_nn_mb  
sqrts_gev

---

## summary.csv

Global statistics:

n_events  
mean_b_fm  
mean_n_part  
mean_n_coll  

---

## event_geometries.jsonl.gz

Each line is a JSON event containing:

event_id  
b_fm  
n_part  
n_coll  

projectile_x_fm  
projectile_y_fm  

target_x_fm  
target_y_fm  

projectile_participant_mask  
target_participant_mask

This allows event‑by‑event geometry analysis.

---

# 6. Example Plots

Typical analysis plots:

1) Impact parameter vs participants  
b vs Npart scatter plot

2) Event geometry  
x vs y scatter plot of nucleon positions

3) Distributions

Histograms of:

- b
- Npart
- Ncoll

---

# 7. Installation

conda env create -f environment.yml
conda activate mcglauber
pip install -e .

---

# 8. Running the Simulation

mcglauber --config config/default.yaml

Outputs will appear in

outputs/

---

# 9. Possible Extensions

Future developments may include:

- eccentricities (epsilon_n)
- participant plane
- initial energy density
- nuclear deformation
- sub‑nucleon structure

---

# 10. References

Miller et al.  
Glauber modeling in high energy nuclear collisions  
Annual Review of Nuclear and Particle Science

Loizides et al.  
Improved Monte Carlo Glauber model

PHOBOS Collaboration documentation
