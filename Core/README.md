# Core Module

The `Core/` directory provides the fundamental implementation of the
information dynamics framework.

It defines the mathematical and computational structure underlying
all simulations in `on_Equations/` and `on_Model/`.

---

## Conceptual Overview

The framework treats information-theoretic quantities as **dynamical variables**
defined on a network.

For each node and link, the following variables are considered:

- Entropy: `H`
- Mutual Information: `MI`
- Transfer Entropy: `TE`
- Reversed Transfer Entropy: `rTE`

These variables evolve in discrete time according to **information dynamic equations**.

---

## Information Dynamic Equations

The evolution is governed by update rules of the form:

- Local balance of incoming and outgoing information flows
- Node-level source/sink term (multivariate effects): `E`
- Control parameters: `α` (alpha terms)

The equations define a closed dynamical system without requiring:
- master equations
- Fokker–Planck equations

---

## Role of Control Parameters (α)

The parameters:

- `α1`: node-level control (source/sink adjustment)
- `α2`: mutual information adjustment
- `α3`: transfer entropy control (forward flow)
- `α4`, `α5`: auxiliary coupling terms
- `α6`: reversed transfer entropy control

These parameters act as **external controls or potentials** that modify
information flow dynamics.

They can be:
- fixed
- time-dependent
- solved under constraints (e.g., blocking flows)

---

## Blocking Flow Condition

The framework allows imposing constraints such as:

> selected transfer entropy flows are forced to vanish

This is implemented by solving for appropriate `α3` and `α6` values
subject to consistency conditions across the network.

This feature is essential for:
- studying constrained information circulation
- analyzing network-level flow control
- constructing stationary solutions

---

## File Structure

Key components inside `Core/`:

- `Information_Dynamic_Equation.py`
  - Implements update rules for `MI`, `TE`, `rTE`, `H`

- `Information_Network.py`
  - Defines network structure (nodes, links, neighbors)

- `Model_Basics.py`
  - Base class for simulation workflows

- `Estimators/`
  - Estimation methods for information-theoretic quantities

---

## Design Philosophy

- **Modular**: equations, estimators, and models are separated
- **Extensible**: new models or estimators can be added easily
- **Dual approach**:
  - direct equation-based dynamics (`on_Equations`)
  - data-driven estimation (`on_Model`)

---

## Notes

- All updates are discrete-time.
- The framework assumes consistent indexing of variables over time.
- Care must be taken when mixing realtime and post-analysis modes.

---

## Relation to Manuscript

This module implements the theoretical framework developed in the manuscript:

> "Dynamical Equations of Mutual Information and Transfer Entropy in Discrete Time"

The variables and update rules correspond directly to the equations
introduced in that work.
