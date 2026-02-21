# InfoDyn_lib

Core library used by the model examples in `on_Model/`.

## Key modules

- `Model_Basics.py`  
  Base class `Model_Basic` providing simulation loops, ensemble construction, and output utilities.

- `Information_Network.py`  
  Defines `A_Node`, `A_Link`, and `A_Network` containers for organizing information variables and α-terms.

- `Estimators/`  
  Estimation backends (discrete binning, KSG/kNN, and composite variables).

## Design intent

Model folders (e.g., `004_*`, `005_*`) should implement **dynamics** and call into InfoDyn_lib for:

- generating ensembles (realtime or post-analysis),
- estimating information variables,
- storing results in a consistent structure.
