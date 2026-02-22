# InfoDyn_lib

Core library for computing information-theoretic quantities in networked dynamical systems.

This module provides:

- Network abstraction
- Simulation engine
- Information estimators
- Multi-variable information utilities

It is designed to support both discrete and continuous models in `on_Model/`.

---

## Structure

InfoDyn_lib/ │ 

             ├── Information_Network.py 
             
             ├── Model_Basics.py 
             
             └── Estimators/ ├── Estimator_Basics.py 
             
                               ├── Simple_Binning.py 
                               
                               ├── KSG.py 
                               
                               └── Several_Information_Variables.py
---

## Core Components

### 1. Information_Network.py

Defines:

- `A_Node`
- `A_Link`
- `A_Network`

Responsible for:

- Storing entropy, mutual information, and transfer entropy values
- Managing network topology
- Computing link-level information variables

---

### 2. Model_Basics.py

Provides the simulation framework:

- Ensemble construction
- Time evolution control
- Realtime vs post-analysis modes
- Data saving utilities

All models inherit from `Model_Basic`.

---

## Estimators

All estimators inherit from `Estimator_Basics.Estimator`.

### Simple_Binning

- Histogram-based estimator
- Designed for discrete systems (Boolean, small Q)
- Efficient for large ensembles
- Used in Model 004

Supports:

- Entropy
- Conditional entropy
- Mutual information
- Multi-variable mutual information

---

### KSG (k-Nearest Neighbor Estimator)

Continuous-variable estimator based on:

Kraskov, A., Stögbauer, H., & Grassberger, P. (2004).  
*Estimating mutual information*. Physical Review E, 69(6), 066138.

Features:

- Chebyshev metric
- Supports:
  - Entropy
  - Mutual information
  - Conditional mutual information
- Designed for ensemble-based post-analysis
- Used in Model 005

---

### Several_Information_Variables

Provides additional composite information measures, including:

- Higher-order entropies
- Multi-variable transfer entropy–like quantities
- Extended network information terms

---

## Workflow Design

Two estimation modes are supported:

### Realtime Mode

- Information measures computed during simulation
- Used primarily with `Simple_Binning`

### Post-Analysis Mode

- Ensemble saved to disk
- Information measures computed afterward
- Used with `KSG` for high-dimensional continuous systems

---

## Design Philosophy

This library is built to:

- Separate simulation from estimation
- Support arbitrary network topologies
- Enable multi-variable conditioning
- Scale from pairwise to network-level analysis
- Remain modular for research extensions
