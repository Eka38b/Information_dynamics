# on_Model

Model-specific implementations built on top of the `InfoDyn_lib` core engine.

This directory contains concrete dynamical systems used to investigate
time-resolved information-theoretic quantities in non-stationary,
discrete-time networks.

Each model folder defines:

- A network topology
- A discrete-time state update rule
- Ensemble simulation parameters
- Time-dependent information analysis

---

## Structure
on_Model/ ├── InfoDyn_lib/        # Core information-theoretic library ├── Utils/              # Utility scripts (e.g., plotting)  └── <Model_Folder>/     # Specific dynamical models
---

## InfoDyn_lib

This subdirectory contains the reusable core framework:

- `Model_Basics.py`  
  Simulation engine for ensemble-based estimation of joint statistics.

- `Entropy.py`  
  Discrete entropy and mutual information primitives.

- `From_Simple_Bin.py`  
  Empirical probability construction from count histograms.

- `Information_Network.py`  
  Node- and link-level information containers (MI, TE, rTE, alpha-terms).

- `Several_Information_Variables.py`  
  Extensions for higher-order and custom information measures.

All models import this library.

---

## Available Models

### 004_ABN_for_GRN

Autonomous Boolean Network (ABN) inspired by gene regulatory network
topologies (Figure-8 structure).

Implements deterministic Boolean update rules and computes:

- Node entropy
- Mutual information
- Transfer entropy
- Reversed transfer entropy
- Higher-order decomposition (alpha-terms)

See:
 on_Model/004_ABN_for_GRN/README.md
 
for model-specific details.

---

## Running a Model

From the repository root:

```bash
python -m on_Model.004_ABN_for_GRN.main
```
Simulation outputs are written to:
 ./Temporal_Results/

---

## Utilities

Utility scripts are provided in:
 on_Model/Utils/

Example:
```bash
python on_Model/Utils/plot_results.py --dir on_Model/004_ABN_for_GRN/Temporal_Results --node A --show
```
