# 001_Toy_Model_A

This directory contains a simple model-based example for studying information dynamics on a directed cycle with an external source.

The model is implemented in `main.py` and defines a cyclic network of `A`-nodes together with one external node `Ext`. The example is intended as a minimal test case for realtime estimation using simple binning.

---

## Overview

`Toy_Model_A` is a discrete-state stochastic model built on the base simulation framework in `Core/Model_Basics`.

The system consists of:

- one external node: `Ext`
- a directed cycle of internal nodes: `A1, A2, ..., AN`

The topology is:

- `Ext -> A1`
- `A1 -> A2 -> ... -> AN -> A1`

Thus, the internal nodes form a directed cycle, while the external node injects an additional signal into `A1`.

---

## Purpose

This model provides a simple setting for studying:

- information flow on a directed cycle
- the effect of an external source on one node
- realtime estimation of information-theoretic quantities
- comparison between internal coupling and external driving

Because the model uses a finite discrete state space and simple binning, it is also useful as a baseline or debugging example.

---

## Dynamics

Each node takes values in a discrete state space of size `Q`.

In the current script:

- `Q = 5`
- the total number of internal nodes is `N`
- the total number of nodes in the network is `N + 1`, including `Ext`

At each time step:

- `Ext` is updated randomly
- each internal node is updated from its own current state and the state of its predecessor on the cycle
- `A1` may also receive input from `Ext`

There are two regimes:

### 1. Before external interaction

For times `t < Start_of_Interaction`:

- the cycle evolves only through internal coupling
- `Ext` does not affect `A1`

### 2. After external interaction begins

For times `t >= Start_of_Interaction`:

- `Ext` influences `A1`
- the cycle is driven by both internal coupling and external input

This makes the model suitable for studying how an external signal modifies information flow in a cyclic system.

---

## Parameters

The constructor is:

```python
Toy_Model_A(n, a, b, c)
```

with:

- `n`: number of internal nodes in the cycle
- `a`: internal coupling coefficient
- `b`: external coupling coefficient
- `c`: internal noise strength

In the script, the default test run is:

```python
Toy_Model_A(5, 0.5, 0.5, 0.2)
```

---

## Estimator

This model uses:

- `Simple_Binning.Estimator(self.Q, 4)`

with:

- discrete state size `Q`
- estimator configuration parameter `4`
- realtime analysis mode

So this example is designed for direct, step-by-step estimation during simulation rather than post-analysis.

---

## Saved output

Results are written to:

```text
./on_Model/001_Toy_Model_A/Temporal_Results/
```

The selected nodes in the script are:

- `A1`
- `AN`

which means the example is set up to track representative node-level behavior at the entry point of the external signal and at the end of the cycle.

---

## Main properties registered by the model

The model stores the following basic metadata:

- model name
- estimator type
- state-space size `Q`
- cycle size `N`
- simulation time limit
- ensemble size

This makes the example suitable for reproducible comparison across parameter choices.

---

## How to run

From the repository root:

```bash
python -m on_Model.001_Toy_Model_A.main
```

---

## Interpretation

This toy model is a minimal example of a cyclic information-processing system with delayed external injection.

It is useful for examining questions such as:

- how transfer entropy changes when an external input is switched on
- how information propagates around a cycle
- how noise affects estimated information flow
- how a simple external perturbation interacts with internal circulation

---

## Notes

- The state space is discrete and finite.
- The external node is purely stochastic in the present implementation.
- The model uses realtime estimation with simple binning.
- Because the system is intentionally simple, it is well suited for testing, debugging, and illustrative figures.
