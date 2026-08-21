# Information Dynamics — Dataset v0.1.3c

## Manuscript
**Robustness of Information Circulation under Entropy Constraints**

This repository contains the datasets and executable scripts used to reproduce the principal numerical results of the manuscript. It includes both stochastic state-space simulations and direct evolution of information-theoretic variables.

---

# Reproduce Figure 3

**Figure 3 is the main manuscript figure demonstrating competition between internal information circulation and an external input at the merging node \(P\).**

Run the following command **from the repository root**:

```bash
python3 -m on_Model.015_Boolean_Probability_Update.main
```

This is the primary reproduction command for the Boolean probability-update model used for **Figure 3**.

The calculation evaluates the relation between:

- the pre-existing circulating transfer entropy, \(T_{A_4\to P}(t_0)\), and
- the newly arriving external transfer entropy, \(T_{\mathrm{Ext}\to P}(t_1)\),

after the external source begins interacting with the merging node \(P\).

The reproduced result should show that increasing the internal circulating flow suppresses the external incoming flow, consistent with the finite-entropy-capacity mechanism discussed in the manuscript.

> **For verification of Figure 3, start with the command above.** The remaining commands in this README reproduce supporting numerical examples used elsewhere in the study.

---

## Overview

The framework consists of two complementary approaches:

- `on_Model/`: data-driven simulations based on stochastic update rules for the underlying state variables.
- `on_Equations/`: direct evolution of entropy, mutual information, transfer entropy, and reversed transfer entropy through closed information-dynamical equations.

The information-theoretic quantities considered are:

- entropy (`H`),
- mutual information (`MI`),
- transfer entropy (`TE`), and
- reversed transfer entropy (`rTE`).

In `on_Model/`, these quantities are estimated from stochastic simulations.
In `on_Equations/`, they are evolved directly from the information-dynamical equations with specified initial conditions.

---

## Prerequisites

- Python >= 3.9
- `numpy`
- `scipy`
- `matplotlib`

Install the required packages with:

```bash
pip install numpy scipy matplotlib
```

All commands below should be executed from the **repository root directory**.

---

## Data Description

The `./Data/` directory contains numerical outputs generated for this study, including results used in the manuscript figures.

Where pre-generated data are included, they can be inspected directly without rerunning the corresponding simulation. Rerunning the scripts provides an independent reproduction of the numerical calculations.

---

# Reproducibility

## 1. Figure 3 — Boolean probability-update model

```bash
python3 -m on_Model.015_Boolean_Probability_Update.main
```

**Purpose**

This simulation reproduces the manuscript's Figure 3, where the cycle

```text
P → A1 → A2 → A3 → A4 → P
```

is initially isolated and the merging node `P` subsequently begins to interact with an external source `Ext`.

**Quantity of interest**

```text
T_{A4→P}(t0)  versus  T_{Ext→P}(t1)
```

**Expected qualitative result**

Increasing the pre-existing internal transfer entropy \(T_{A_4\to P}(t_0)\) suppresses the subsequent external transfer entropy \(T_{\mathrm{Ext}\to P}(t_1)\).

This is the numerical realization of the competing-information-flow mechanism discussed in the manuscript.

---

## 2. Oscillatory dynamics of two interacting cycles

```bash
python3 -m on_Equations.005_Oscillatory_Two_Cycles.main
```

**Expected outcome**

- sustained oscillations in TE and rTE,
- bounded mutual information.

---

## 3. Small deviation from a stationary single cycle

```bash
python3 -m on_Equations.001_A_Single_Cycle.main

python3 -m Utils.plot_results \
  --dir on_Equations/001_A_Single_Cycle/Temporal_Results/ \
  --links A1 A2 A2 A3 A3 A4 A4 A5 A5 A6 A6 A7 A7 A8 A8 A1 \
  --keys MI \
  --paper2
```

**Expected outcome**

- near-stationary mutual information,
- bounded response to a small perturbation.

---

## 4. Transient dynamics with an external information source

```bash
python3 -m on_Model.001_Toy_Model_A.main

python3 -m Utils.plot_results \
  --dir on_Model/001_Toy_Model_A/Temporal_Results/ \
  --links A1 A2 A2 A3 A3 A4 A4 A5 A5 A1 Ext A1 \
  --keys TE2 \
  --paper2
```

**Expected outcome**

- transient TE response after activation of the external input,
- relaxation toward a new circulating state.

---

## Output Structure

A typical simulation output directory has the form:

```text
Temporal_Results/
├── *_E_values.txt
├── *_MI.txt
├── *_TE.txt
└── *.png
```

The exact set of files depends on the simulation or equation module being executed.

---

## Reproducibility Checklist

For manuscript Figure 3:

1. Clone or download the repository.
2. Open a terminal in the repository root.
3. Install the required Python packages.
4. Run:

   ```bash
   python3 -m on_Model.015_Boolean_Probability_Update.main
   ```

5. Inspect the generated output for the relation between \(T_{A_4\to P}(t_0)\) and \(T_{\mathrm{Ext}\to P}(t_1)\).

---

## Latest Updates

For the most recent code, bug fixes, and extended datasets, see the GitHub repository:

https://github.com/Eka38b/Information_dynamics
