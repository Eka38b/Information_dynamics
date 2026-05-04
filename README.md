# Information Dynamics — Dataset v0.1.3

## Manuscript
**Robustness of Information Circulation under Entropy Constraints**

---

## Overview
This repository provides the dataset and executable scripts required to reproduce all key results and figures in the manuscript. The framework consists of two complementary approaches:

- `on_Model/`: Data-driven simulations (stochastic update rules)
- `on_Equations/`: Direct evolution of information-theoretic variables

---
## Core Mechanism

The repository implements a dynamical framework in which information-theoretic quantities—entropy (H), mutual information (MI), transfer entropy (TE), and reversed transfer entropy (rTE)—are treated as state variables that evolve in discrete time.  

Two complementary realizations are provided:
- In `on_Model/`, these quantities are estimated from stochastic simulations of underlying state variables.
- In `on_Equations/`, they evolve directly through closed dynamical equations with specified initial conditions.

Information circulation in network structures (e.g., cycles and interacting loops) is governed by these dynamics under entropy constraints, leading to characteristic behaviors such as stationary states, bounded oscillations, and transient responses to external inputs.

---
## Prerequisites

- Python ≥ 3.9
- Recommended packages:
  - numpy
  - scipy
  - matplotlib

Install via:
```bash
pip install numpy scipy matplotlib
```

---
## Data Description

The `./Data/` directory contains the simulation outputs generated for this study, including all results used to produce the figures in the manuscript. These data files allow direct verification of the reported results without rerunning the simulations.

---

## Reproducibility

The results in the `./Data/` directory are reproducible using the following commands.

---

### 1. Figure 3 (Boolean probability update model)
```bash
python3 -m on_Model.015_Boolean_Probability_Update.main
```

---

### 2. Oscillatory dynamics of two interacting cycles
```bash
python3 -m on_Equations.005_Oscillatory_Two_Cycles.main
```

Expected outcome:
- Sustained oscillations in TE and rTE
- Bounded mutual information

---

### 3. Small deviation in a single stationary cycle
```bash
python3 -m on_Equations.001_A_Single_Cycle.main
python3 -m Utils.plot_results \
  --dir on_Equations/001_A_Single_Cycle/Temporal_Results/ \
  --links A1 A2 A2 A3 A3 A4 A4 A5 A5 A6 A6 A7 A7 A8 A8 A1 \
  --keys MI \
  --paper2
```

Expected outcome:
- Near-stationary MI with small perturbations

---

### 4. Transient dynamics with external information source
```bash
python3 -m on_Model.001_Toy_Model_A.main
python3 -m Utils.plot_results \
  --dir on_Model/001_Toy_Model_A/Temporal_Results/ \
  --links A1 A2 A2 A3 A3 A4 A4 A5 A5 A1 Ext A1 \
  --keys TE2 \
  --paper2
```

Expected outcome:
- Transient TE response due to external input
- Relaxation toward steady circulation

---


## Output Structure

Each simulation generates:
```
Temporal_Results/
├── *_E_values.txt
├── *_MI.txt
├── *_TE.txt
└── *.png
```

---

## Latest Updates

For the most recent updates, bug fixes, and extended versions of the dataset and code, please refer to the GitHub repository:

https://github.com/Eka38b/Information_dynamics

---

