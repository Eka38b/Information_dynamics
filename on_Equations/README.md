# on_Equations

This directory contains examples in which information-theoretic quantities
evolve directly according to dynamical equations.

In contrast to model-based approaches, no underlying physical or stochastic
system is simulated. Instead, the information variables themselves are treated
as primary dynamical variables.

---

## Conceptual Role

The modules in this directory implement the intrinsic dynamics of:

- Entropy (H)
- Mutual Information (MI)
- Transfer Entropy (TE)
- Reversed Transfer Entropy (rTE)

These quantities evolve according to the information dynamic equations
defined in `Core/`.

---

## Key Features

### 1. Direct Equation-Based Evolution

- No trajectory data is generated
- No estimator is required
- Deterministic updates of information variables

### 2. Control Parameters

- alpha1 – alpha6 control the dynamics
- can be fixed or solved under constraints

### 3. Blocking Flow Conditions

- selected TE and rTE flows can be forced to vanish
- enables constrained circulation and consistency analysis

---

## Included Examples

### 001_A_Single_Cycle
- Simple cyclic network
- Demonstrates basic flow circulation
- Useful for verifying consistency

### 002_Cycle_and_Source
- Cycle with an additional source node
- Shows interaction between injection/multivariate effects (E) and flows

### 005_Oscillatory_Two_Cycles
- Two coupled cyclic networks (A-cycle and B-cycle)
- Inter-cycle links: A2 → B2 and B4 → A4
- Dynamic feedback through node-level E terms
- Oscillatory exchange between cycles via TE and rTE
- Useful for studying:
  - coupled circulation dynamics
  - balance between TE and rTE across subsystems
  - feedback-controlled information flow

---

## How to Run

```bash
python -m on_Equations.001_A_Single_Cycle.main
python -m on_Equations.002_Cycle_and_Source.main
python -m on_Equations.005_Oscillatory_Two_Cycles.main
```

---

## Output

- Time series of:
  - MI
  - TE
  - rTE
  - H
  - alpha parameters

---

## When to Use This Module

- Analyze intrinsic dynamics
- Study constrained flows
- Explore theoretical properties without noise

---

## Relation to on_Model

- on_Equations: intrinsic dynamics
- on_Model: data-driven estimation

---

## Notes

- Initial conditions are critical
- Stability depends on alpha parameters
- Blocking constraints may introduce nontrivial coupling
- 
