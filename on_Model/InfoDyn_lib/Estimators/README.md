# Estimators

Estimator backends for computing information-theoretic quantities.

## Available estimators

- `Simple_Binning.py`  
  Histogram/binning estimator for discrete variables (realtime updates; exact up to binning).

- `KSG.py`  
  kNN / KSG-style estimators for continuous variables (post-analysis ensembles).

- `Several_Information_Variables.py`  
  Helper classes for derived/composite variables built on top of base estimators.

## Conventions

- **Realtime** estimators update internal statistics at each simulation step.
- **Post-analysis** estimators read saved ensemble files and compute quantities offline.
