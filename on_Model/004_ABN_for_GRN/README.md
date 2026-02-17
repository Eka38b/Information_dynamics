# 004_ABN_for_GRN  
**Autonomous Boolean Network (ABN) Model for Gene Regulatory Networks**  
Information-Theoretic Analysis via Ensemble Dynamics

---

## Overview

This module implements an Autonomous Boolean Network (ABN) inspired by the
Figure-8 topology introduced in:

> M. Sun, X. Cheng, and J. E. S. Socolar,  
> *Causal structure of oscillations in gene regulatory networks*,  
> CHAOS 23, 025104 (2013)

The purpose of this implementation is not merely to simulate Boolean dynamics,
but to extract **time-resolved information-theoretic quantities** from ensemble
statistics, including:

- Shannon entropy
- Mutual information
- Conditional mutual information
- Transfer entropy (TE)
- Reversed transfer entropy (rTE)
- Higher-order multivariate mutual information
- Information-flow decompositions (α-terms)

This folder represents a computational bridge between
Boolean network dynamics and information thermodynamics.

---

## Model Description

The topology consists of:

- A central node `A`
- Two directed chains:
  - `B1 → B2 → ... → Bn`
  - `C1 → C2 → ... → Cm`
- Feedback connections:
  - `B1 ↔ A`, `Bn ↔ A`
  - `C1 ↔ A`, `Cm ↔ A`

The update rules are deterministic Boolean transitions.

Ensemble simulations generate empirical joint distributions
of the form:

\[
p(x_t, y_t, x_{t+1}, y_{t+1})
\]

which are then used to compute dynamical information measures.

---

## Information-Theoretic Quantities

For each link (X, Y), the following quantities are computed:

- \( H(X) \), \( H(Y) \)
- \( I(X;Y) \)
- \( T_{Y\to X} = I(Y;X'|X) \)
- Reversed transfer entropy
- Higher-order interaction information
- α-terms corresponding to partial information flows

These quantities are computed from ensemble-based empirical
probability distributions using exact counting.

---

## Computational Strategy

The simulation framework:

- Uses ensemble sampling of size `E`
- Accumulates joint counts over \( (x,y,x',y') \)
- Computes information measures at each time step
- Saves time-resolved results to disk

The implementation supports blockwise streaming for
memory-controlled computation when alphabet size \( Q \) is large.

---

## Purpose of This Module

This module is designed to investigate:

- Directionality of information flow
- Emergence of causal structure
- Decomposition of entropy production
- Higher-order dynamical dependencies

It serves as a concrete testbed for
non-equilibrium information dynamics in discrete systems.

---

## Usage

```bash
python main.py
