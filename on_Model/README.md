# on_Model

This folder contains **model examples** and the reusable **InfoDyn_lib** toolkit used by the
*Information_dynamics* project (information theory on non‑stationary / dynamical time series).

## Structure

- `004_ABN_model_of_GRN/`  
  Discrete **Autonomous Boolean Network** (ABN) example for a gene regulatory network (GRN).  
  Uses the `Simple_Binning` estimator for realtime histogram-based estimation.

- `005_Three_Nodes_GRN (based on Qiao et al., 2022)/`  
  Continuous **three-node GRN motif** example.  
  Saves ensembles and computes information measures in **post-analysis** (e.g., with `KSG`).

- `InfoDyn_lib/`  
  Shared library code (simulation scaffolding + estimators + information-network objects).

## Running

Most models can be run from within the repository root (so `on_Model` is importable):

```bash
cd Information_dynamics
python -m on_Model.004_ABN_model_of_GRN.main
python -m on_Model.005_Three_Nodes_GRN.main
```

Model scripts typically write outputs into `Temporal_Results/` and/or `C*_Ensemble/` folders.

## Notes

- Realtime (binning) estimators are best for discrete state spaces with modest alphabet size `Q`.
- kNN/KSG estimators are best for continuous variables but may have high variance in large dimensions.
