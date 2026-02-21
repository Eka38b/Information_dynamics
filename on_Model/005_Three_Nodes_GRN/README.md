# 005_Three_Nodes_GRN

Three-node GRN motif model (continuous variables) with ensemble saving and post-analysis estimation.

## What it does

- Simulates a 3-node GRN motif (parameters typically loaded from `data_ex.mat`).
- Saves ensembles to `C*_Ensemble/` directories.
- Computes information measures in post-analysis (e.g., using `KSG`).

## Outputs

- `C1_Ensemble/` ... `C5_Ensemble/`  
  Saved ensemble snapshots (one file per saved time index).

- `Temporal_Results/`  
  Time series of computed information variables.

## References

- Qiao, L., Zhang, Z.-B., Zhao, W., Wei, P., & Zhang, L. (2022). Network design principle for robust oscillatory behaviors with respect to biological noise. eLife, 11, e76188. https://doi.org/10.7554/eLife.76188
