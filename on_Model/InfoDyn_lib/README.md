---
# InfoDyn_lib  
Core Library for Discrete-Time Information Dynamics
---

## Philosophy

`InfoDyn_lib` provides a modular framework for computing
information-theoretic quantities from empirical discrete-time
ensemble statistics.

The library is intentionally:

- Explicit
- Transparent
- Non-black-box
- Based directly on count histograms

It is designed for research in:

- Information thermodynamics
- Transfer entropy
- Causal inference in dynamical systems
- Multivariate information decomposition

---

## Architecture

### 1. From_Simple_Bin.py
Implements empirical probability distribution generation from raw counts.

### 2. Entropy.py
Provides:

- Shannon entropy
- Conditional entropy
- Mutual information
- Multivariate mutual information (recursive definition)

### 3. Information_Network.py
Defines:

- Nodes
- Links
- Computation of:
  - TE
  - reversed TE
  - α-terms
  - partial information contributions

### 4. Several_Information_Variables.py
Extensible framework for additional dynamical information quantities.

---

## Mathematical Basis

All measures are computed from empirical distributions:

\[
p(x,y,x',y')
\]

No approximations or Gaussian assumptions are used.

Multivariate mutual information is implemented recursively
via conditional mutual information differences.

---

## Design Principles

- Ensemble-based estimation
- Explicit probability construction
- Modular separation between:
  - Dynamics
  - Statistics
  - Information evaluation
- Extensible to arbitrary discrete alphabet size \( Q \)

---

## Intended Applications

- Boolean networks
- Discrete Markov systems
- Cellular automata
- Gene regulatory models
- Nonequilibrium information flow analysis
