# on_Equations

This directory contains examples in which information-theoretic quantities
evolve directly according to dynamical equations.

In contrast to model-based approaches, no underlying physical or stochastic
system is simulated. Instead, the information variables themselves are treated
as primary dynamical variables.

---

## Conceptual Role

The modules in this directory implement the **intrinsic dynamics** of:

- Entropy (H)
- Mutual Information (MI)
- Transfer Entropy (TE)
- Reversed Transfer Entropy (rTE)

These quantities evolve according to the information dynamic equations
defined in `Core/`.

This approach allows one to study:

- the structure of information flow independent of specific models
- the role of control parameters (α)
- constrained dynamics such as blocked flows
- stationary and self-consistent solutions

---

## Key Features

### 1. Direct Equation-Based Evolution

The system evolves by iterating update equations:

- No trajectory data is generated
- No estimator is required
- All variables are updated deterministically

This provides a clean setting for analyzing the mathematical structure
of the framework.

---

### 2. Control Parameters

The α-parameters (α1–α6) can be specified explicitly or solved under constraints.

Typical uses include:
- fixing certain flows
- enforcing conservation-like conditions
- exploring parameter regimes

---

### 3. Blocking Flow Conditions

A central feature in these examples is the ability to impose:

> selected transfer entropy flows vanish

This is achieved by solving for α-parameters such that:

    TE_{i→j}(t+1) = 0

for chosen directed edges.

This enables:
- construction of constrained networks
- study of circulation and flow suppression
- analysis of compatibility conditions across nodes

---

## Included Examples

### 001_A_Single_Cycle

- Simple cyclic network
- Demonstrates basic flow circulation
- Useful for verifying consistency of update rules

### 002_Cycle_and_Source

- Combines cyclic structure with a source node
- Illustrates interaction between local injection (E) and flow dynamics
- Shows nontrivial behavior under mixed topology

---

## How to Run

From the repository root:

```bash
python -m on_Equations.001_A_Single_Cycle.main
```

or

```bash
python -m on_Equations.002_Cycle_and_Source.main
```

---

## Output

- Results are stored in corresponding subdirectories
- Variables are recorded over time:
  - MI
  - TE
  - rTE
  - H
  - α parameters

---

## When to Use This Module

Use `on_Equations` when you want to:

- study the **mathematical properties** of the framework
- test theoretical predictions
- analyze constrained dynamics without model-specific noise
- explore parameter dependence systematically

---

## Relation to on_Model

- `on_Equations`: intrinsic, equation-driven dynamics
- `on_Model`: data-driven estimation from simulated systems

Together, they provide complementary validation of the framework.

---

## Notes

- Initial conditions must be specified carefully.
- Stability and boundedness depend on chosen α parameters.
- Blocking conditions may introduce nontrivial consistency constraints.
- 
