# Information Dynamics

[![DOI](https://zenodo.org/badge/1159713412.svg)](https://doi.org/10.5281/zenodo.18817495)

A computational framework for studying the dynamics of information-theoretic quantities in non-stationary networked systems.

The repository combines reusable Python modules, model-based simulations, direct information-dynamical equations, archived numerical data, and the manuscripts developed with the framework. The principal quantities are entropy ($H$), mutual information ($I$), transfer entropy ($T$), and reversed transfer entropy ($T^{\dagger}$).

This archive corresponds to version **v0.1.4b**.

## Framework

The project provides two complementary approaches:

| Approach | Directory | Description |
| --- | --- | --- |
| Model-based analysis | [`on_Model/`](on_Model/) | Simulates explicit stochastic or deterministic systems and estimates information-theoretic quantities from ensemble time series. |
| Equation-based analysis | [`on_Equations/`](on_Equations/) | Evolves the information-theoretic quantities directly from information-dynamical equations and specified initial conditions. |

Both approaches use the network structures and computational components in [`Core/`](Core/). The model-based workflow also uses the estimators in [`Core/Estimators/`](Core/Estimators/), including simple binning for discrete systems and a KSG-type nearest-neighbor estimator for continuous systems.

The framework is intended for investigations of:

- time-dependent information measures in non-stationary systems;
- information circulation and control on networks;
- transfer entropy and reversed transfer entropy;
- constrained or blocked information flows;
- discrete- and continuous-state dynamical models; and
- relations between information dynamics, complex systems, and information thermodynamics.

## Repository Structure

| Path | Contents |
| --- | --- |
| [`Core/`](Core/) | Network classes, simulation infrastructure, information-dynamical equations, and estimators. |
| [`on_Model/`](on_Model/) | Explicit dynamical models from which information quantities are estimated. |
| [`on_Equations/`](on_Equations/) | Examples that evolve information quantities directly. |
| [`Data/`](Data/) | Archived outputs associated with selected models, equation examples, and manuscript figures. |
| [`Utils/`](Utils/) | Plotting tools and estimator-credibility diagnostics. |
| [`Manuscripts/`](Manuscripts/) | Published and preprint manuscripts associated with the project. |

More detailed documentation is provided in the README file within each major directory.

## Included Examples

### Model-based simulations

| Module | Main purpose |
| --- | --- |
| [`001_Toy_Model_A`](on_Model/001_Toy_Model_A/) | A discrete information cycle perturbed by an external source. |
| [`004_ABN_for_GRN`](on_Model/004_ABN_for_GRN/) | An autonomous Boolean-network model of a figure-eight gene-regulatory network. |
| [`005_Three_Nodes_GRN`](on_Model/005_Three_Nodes_GRN/) | A continuous three-node gene-regulatory model analyzed with KSG-type estimation. |
| [`015_Boolean_Probability_Update`](on_Model/015_Boolean_Probability_Update/) | A probabilistic Boolean example of competition between internal and external information inputs. |
| [`019_Fredkin_Switch_Gate`](on_Model/019_Fredkin_Switch_Gate/) | A finite-state reversible model using a Fredkin controlled-swap interaction at a merging node. |

### Direct information-equation examples

| Module | Main purpose |
| --- | --- |
| [`001_A_Single_Cycle`](on_Equations/001_A_Single_Cycle/) | Information-variable evolution on a single directed cycle. |
| [`002_Cycle_and_Source`](on_Equations/002_Cycle_and_Source/) | A directed cycle interacting with an additional information source. |
| [`005_Oscillatory_Two_Cycles`](on_Equations/005_Oscillatory_Two_Cycles/) | Oscillatory transfer entropy, reversed transfer entropy, and mutual information in two coupled cycles. |

## Model 019 and Manuscript 002

[`on_Model/019_Fredkin_Switch_Gate/`](on_Model/019_Fredkin_Switch_Gate/) is the numerical model developed for the manuscript in [`Manuscripts/002/`](Manuscripts/002/), *Information Circulation and External-Flow Suppression under Finite Capacity*.

Model 019 provides the current numerical construction and Figure 3 dataset for that manuscript. It studies competition between a pre-existing circulating transfer entropy and a newly activated external transfer entropy at the merging node $p$. The released outputs are stored in [`Data/on_Model019/`](Data/on_Model019/). Model 015 and its archived outputs are retained as an earlier numerical example.

To regenerate the Model 019 results, run from the repository root:

```bash
python3 -m on_Model.019_Fredkin_Switch_Gate.main
```

The model-specific assumptions, parameterization, analytical prediction, and output structure are documented in its [README](on_Model/019_Fredkin_Switch_Gate/README.md).

## Manuscripts

The repository currently includes:

| Directory | Work |
| --- | --- |
| [`Manuscripts/001/`](Manuscripts/001/) | *Dynamical Equations of Mutual Information and Transfer Entropy in Discrete Time* (published article). |
| [`Manuscripts/002/`](Manuscripts/002/) | *Information Circulation and External-Flow Suppression under Finite Capacity* (preprint). |
| [`Manuscripts/003/`](Manuscripts/003/) | *A Correlation-Production Reformulation of the Transfer-Entropy Second Law of Information Thermodynamics* (preprint). |
| [`Manuscripts/005/`](Manuscripts/005/) | *A Directed Hypergraph Representation of Higher-Order Information Flows* (preprint). |

## Installation

Python 3.9 or later is recommended. Install the required packages with:

```bash
python3 -m pip install -r requirements.txt
```

The main dependencies are NumPy, SciPy, scikit-learn, and Matplotlib.

Run all module commands from the repository root so that package imports and relative output paths resolve correctly.

## Running the Examples

Representative commands are:

```bash
# Model-based simulations
python3 -m on_Model.001_Toy_Model_A.main
python3 -m on_Model.004_ABN_for_GRN.main
python3 -m on_Model.005_Three_Nodes_GRN.main
python3 -m on_Model.015_Boolean_Probability_Update.main
python3 -m on_Model.019_Fredkin_Switch_Gate.main

# Direct information-equation examples
python3 -m on_Equations.001_A_Single_Cycle.main
python3 -m on_Equations.002_Cycle_and_Source.main
python3 -m on_Equations.005_Oscillatory_Two_Cycles.main
```

Individual modules may have additional requirements, parameters, or plotting steps. Consult their README files before running a complete numerical experiment.

## Data and Outputs

New calculations are generally written to a module-specific `Temporal_Results/` directory. Reference outputs from selected calculations are preserved separately under [`Data/`](Data/) so that released results remain available for inspection and comparison.

The archived datasets include:

- `Data/on_Model001/`, `Data/on_Model004/`, `Data/on_Model015/`, and `Data/on_Model019/`;
- `Data/on_Equations001/` and `Data/on_Equations005/`; and
- text files containing node- and link-level quantities, simulation properties, and generated figures.

Because some simulations use finite ensembles and time-dependent random seeds, a new run may not reproduce every numerical value exactly. See the relevant model README for the expected analytical or qualitative behavior.

## Utilities

Plot stored node- or link-level results with [`Utils/plot_results.py`](Utils/plot_results.py). For example:

```bash
python3 -m Utils.plot_results \
  --dir Data/on_Equations001/ \
  --links A1 A2 A2 A3 A3 A4 A4 A5 A5 A6 A6 A7 A7 A8 A8 A1 \
  --keys MI
```

[`Utils/estimator_credibility.py`](Utils/estimator_credibility.py) provides bootstrap intervals, permutation tests, subsample-stability checks, parameter-sensitivity checks, and synthetic benchmarks for the implemented estimators.

## Citation

If you use this repository, please cite the appropriate archived release and any associated manuscript. Citation metadata for the software are provided in [`CITATION.cff`](CITATION.cff).

The current repository record is available at [Zenodo](https://doi.org/10.5281/zenodo.18817495), and the latest code is maintained on [GitHub](https://github.com/Eka38b/Information_dynamics).

## License

The source code is released under the [MIT License](LICENSE). Manuscript PDFs may have separate terms stated in the corresponding manuscript directories.
