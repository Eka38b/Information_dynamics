# Information Dynamics — Dataset v0.1.4

## Manuscript
**Robustness of Information Circulation under Entropy Constraints**

This repository contains the datasets and executable scripts used to reproduce the principal numerical results of the manuscript. It includes both stochastic state-space simulations and direct evolution of information-theoretic variables.

In v0.1.4, the finite-state reversible model in `on_Model/019_Fredkin_Switch_Gate/` replaces Model 015 as the source of Figure 3. Model 015 and its archived outputs are retained as an earlier numerical example.

---

# Reproduce Figure 3

**Figure 3 demonstrates competition between internal information circulation and an external input at the merging node $p$ in a finite-state reversible Fredkin switch-gate model.**

Run the following command **from the repository root**:

```bash
python3 -m on_Model.019_Fredkin_Switch_Gate.main
```

This is the primary reproduction command for **Figure 3**. The released data and figure are archived under

```text
Data/on_Model019/
```

New simulation outputs are written under

```text
on_Model/019_Fredkin_Switch_Gate/Temporal_Results/
```

The calculation evaluates the relation between:

- the pre-existing circulating transfer entropy, $T_{A_3\to p}(t_0)$, and
- the newly arriving external transfer entropy, $T_{\mathrm{Ext}\to p}(t_1)$,

after the external source begins interacting with the merging node $p$.

The model realizes the capacity relation

$$
T_{A_3\to p}(t_0)+T_{\mathrm{Ext}\to p}(t_1)=\ln 4,
$$

up to finite-sample estimation error. Thus, increasing the pre-existing circulating flow suppresses the newly arriving external flow.

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
- packages listed in `requirements.txt`

Install the required packages with:

```bash
python3 -m pip install -r requirements.txt
```

All commands below should be executed from the **repository root directory**.

---

## Data Description

The `./Data/` directory contains numerical outputs generated for this study, including results used in the manuscript figures. In particular, `Data/on_Model019/` contains the five-trial, ten-parameter dataset and `Figure3.png` generated with the Fredkin switch-gate model.

Where pre-generated data are included, they can be inspected directly without rerunning the corresponding simulation. Rerunning the scripts provides an independent reproduction of the numerical calculations.

---

# Reproducibility

## 1. Figure 3 — Fredkin switch-gate model

```bash
python3 -m on_Model.019_Fredkin_Switch_Gate.main
```

**Purpose**

This simulation reproduces the manuscript's Figure 3, where the isolated cycle

```text
p → A1 → A2 → A3 → p
```

is initially stationary. At the specified interaction time, the first bit of the external node `Ext` controls whether the two bits of `A3` are exchanged before being written to the merging node `p`. The resulting complete state update is bijective.

**Quantity of interest**

```text
T_{A3→p}(t0)  versus  T_{Ext→p}(t1)
```

**Expected qualitative result**

The numerical estimates follow a decreasing relation close to

```text
T_{A3→p}(t0) + T_{Ext→p}(t1) = ln(4).
```

This is the reversible numerical realization of the finite-entropy-capacity mechanism discussed in the manuscript. For the analytical construction, parameterization, and numerical details, see `on_Model/019_Fredkin_Switch_Gate/README.md`.

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
   python3 -m on_Model.019_Fredkin_Switch_Gate.main
   ```

5. Inspect `on_Model/019_Fredkin_Switch_Gate/Temporal_Results/Figure3.png` for the relation between $T_{A_3\to p}(t_0)$ and $T_{\mathrm{Ext}\to p}(t_1)$. The released reference output is `Data/on_Model019/Figure3.png`.

---

## Latest Updates

For the most recent code, bug fixes, and extended datasets, see the GitHub repository:

https://github.com/Eka38b/Information_dynamics
