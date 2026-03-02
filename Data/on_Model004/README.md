# Model 004 — ABN for GRN  
Reproducible Data and Figure Generation

This directory contains the simulation outputs and processed datasets
corresponding to **Model 004 (ABN for GRN)** used in the manuscript:

> “Dynamical Equations of Mutual Information and Transfer Entropy on Discrete Time”

This release (v0.1.1) guarantees reproducibility of the numerical results
and figures reported in the paper.

---

## Environment

All commands should be executed from the **root directory** of the repository.

Required dependencies are listed in:

requirements.txt

---

## Step 1 — Generate Temporal Simulation Data

Run:

python -m on_Model.004_ABN_for_GRN.main

This command:

- Executes the ABN simulation
- Produces temporal results
- Stores outputs in:

on_Model/004_ABN_for_GRN/Temporal_Results/

---

## Step 2 — Reproduce Link-Based Figures

To generate figures corresponding to specific regulatory links:

python -m on_Model.Utils.plot_results \
  --dir on_Model/004_ABN_for_GRN/Temporal_Results/ \
  --link B4 B5 \
  --paper

This command reproduces link-level results used in the manuscript.

---

## Step 3 — Reproduce Node-Based Figures

To generate node-level plots:

python -m on_Model.Utils.plot_results \
  --dir on_Model/004_ABN_for_GRN/Temporal_Results/ \
  --node B1 \
  --paper

This command reproduces node-level temporal dynamics
as presented in the paper.

---

## Output

Generated figures are saved in the corresponding results directory.

---

## Notes

- The `--paper` flag ensures publication-style formatting.
- Results are deterministic given identical environment and parameters.
- This version (v0.1.1) corresponds exactly to the archived Zenodo dataset.
