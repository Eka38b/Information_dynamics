# Information_dynamics

A computational framework for studying **information-theoretic dynamics in non-stationary systems**, including entropy, mutual information, transfer entropy, and derived dynamical quantities on discrete-time models.

This repository provides:

- A reusable information-theoretic computation library
- Modular simulation frameworks for networked dynamical systems
- Example network models
- Support for both discrete and continuous-state systems
- Real-time and post-analysis estimation workflows

---

##  Project Motivation

Modern complex systems — biological, physical, and engineered — exhibit structured information flow across time and network topology.

This project aims to:

- Quantify **time-dependent information measures**
- Derive and analyze **dynamical equations of information quantities**
- Study **transfer entropy and reversed transfer entropy**
- Explore **network-level information interactions**
- Provide computational tools for ensemble-based estimation

The framework is designed to support ongoing research into:

- Information dynamics beyond bipartite systems
- Network topology effects on information propagation
- Entropy production and fluctuation relations
- Non-stationary stochastic processes

---

##  Repository Structure

Information_dynamics/ │ 

                      ├── on_Model/ │   
                      
                                      ├── 004_ABN_for_GRN/ │   
                                      
                                      ├── 005_Three_Nodes_GRN/ │   
                                      
                                      └── InfoDyn_lib/ │
---

### `on_Model/`
Contains concrete model implementations and the core information-dynamics library.

### `InfoDyn_lib/`
Reusable infrastructure including:

- Network representation (`Information_Network.py`)
- Simulation engine (`Model_Basics.py`)
- Estimators:
  - `Simple_Binning` (discrete histogram estimator)
  - `KSG` (k-nearest neighbor estimator for continuous variables)
  - Additional multi-variable information tools

---

##  Estimation Methods

Two primary estimation strategies are implemented:

### 1 Simple Binning (Discrete Systems)

- Histogram-based counting
- Efficient for Boolean or small-Q systems
- Suitable for Autonomous Boolean Networks (ABN)

### 2 KSG (Continuous Systems)

- k-nearest neighbor estimator
- Chebyshev metric
- Supports:
  - Entropy
  - Mutual Information
  - Conditional Mutual Information
- Designed for ensemble-based non-stationary analysis

---

##  Implemented Models

###  Model 004 — Autonomous Boolean Network (ABN)

Figure-8 structured gene regulatory network using Boolean dynamics.

Based on:

Sun, M., Cheng, X., & Socolar, J. E. S. (2013).  
*Causal structure of oscillations in gene regulatory networks: Boolean analysis of ordinary differential equation attractors*.  
Chaos, 23(2), 025104.  
https://doi.org/10.1063/1.4807733

Uses:
- Discrete states
- Ensemble histogram estimation

---

###  Model 005 — Three-Node GRN (Continuous)

Three-node gene regulatory motif with stochastic/ODE dynamics.

Based on:

Qiao, L., Zhang, Z.-B., Zhao, W., Wei, P., & Zhang, L. (2022).  
*Network design principle for robust oscillatory behaviors with respect to biological noise*.  
eLife, 11, e76188.  
https://doi.org/10.7554/eLife.76188

Uses:
- Continuous dynamics
- KSG estimator (post-analysis workflow)

---

##  Workflow Modes

The framework supports two analysis modes:

###  Realtime Mode
- Compute information measures during simulation
- Suitable for discrete systems

###  Post-Analysis Mode
- Store ensemble data
- Compute high-dimensional estimators afterward
- Suitable for continuous models and KSG

---

##  Research Scope

This repository supports research on:

- Dynamical equations of mutual information
- Transfer entropy and reversed transfer entropy
- Conditional information flows
- High-dimensional conditioning effects
- Network-based information decomposition

It is actively used for developing a generalized framework for information-theoretic state variables in networked systems.

---


## Quick start

### 1) Run a model
Example (ABN model):
```bash
cd Information_dynamics
python -m on_Model.004_ABN_for_GRN.main
```
