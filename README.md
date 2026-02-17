# Information_dynamics
Information theory on non-stationary discrete-time dynamical systems.

This repository provides a research-oriented framework to:
- simulate discrete-time network dynamics (Boolean and multi-alphabet models),
- estimate empirical joint distributions from ensembles,
- compute information-theoretic measures over time (entropy, MI, TE, reversed TE),
- and explore decomposition terms (alpha-terms) related to information flow.

---

## What’s inside

### `on_Model/`
Model-specific implementations and experiments.

- `004_ABN_for_GRN/`  
  Autonomous Boolean Network (ABN) for a gene-regulatory-network-like topology,
  with time-resolved information dynamics computed from ensemble statistics.

### `InfoDyn_lib/` 
Core utilities to compute information measures from empirical distributions:
- probability construction from counts,
- entropy / conditional entropy / mutual information,
- multivariate mutual information (recursive),
- network objects (node/link variables, TE/rTE, alpha-terms),
- optional extra information variables.

---

## Quick start

### 1) Run a model
Example (ABN model):
```bash
cd on_Model
python -m 004_ABN_for_GRN.main.py
