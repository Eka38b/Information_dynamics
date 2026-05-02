# 015_Boolean_Probability_Update

Boolean probability-update model for testing competing transfer-entropy flows into a finite-capacity node.

## Overview

This directory implements a discrete Boolean network in which an internal circulation and an external random source both influence a target node `p`. The model is designed to examine how an existing internal information flow into `p` competes with a newly introduced external information flow.

The main comparison produced by the script is

$T_{A4 \to p}(t_0) \quad \text{vs.} \quad T_{Ext \to p}(t_1)$,

where the internal link `A4 -> p` is measured immediately before the external interaction begins, and the external link `Ext -> p` is measured immediately after that interaction is introduced.

## Network structure

For the default setting `N = 4`, the model uses the Boolean nodes

```text
Ext, p, A1, A2, A3, A4
```

with directed links

```text
A1 -> A2 -> A3 -> A4 -> p -> A1
Ext -> p
```

Thus, `A1, ..., A4, p` form a directed circulation, while `Ext` acts as an external Boolean source coupled to the merging node `p`.

## State dynamics

All nodes are Boolean-valued, with state space size `Q = 2`.

At each time step, the circulation updates deterministically by shifting the previous state forward:

```text
A(i+1)(t+1) = Ai(t),   i = 1, ..., N-1
A1(t+1)     = p(t)
```

The external source is independently resampled at each time step:

```text
Ext(t+1) ~ Bernoulli(0.5)
```

The target node `p` is updated probabilistically. Before the external interaction begins,

```text
P[p(t+1)=1] = exp(- beta_Int * A_N(t)).
```

After `Start_of_Interaction`, the external source also suppresses the update probability:

```text
P[p(t+1)=1] = exp(- beta_Int * A_N(t) - beta_Ext * Ext(t)).
```

Here, `beta_Int` controls the strength of the internal input from `A_N`, while `beta_Ext` controls the strength of the external input from `Ext`.

## Main parameters

| Parameter | Default / script value | Meaning |
|---|---:|---|
| `Q` | `2` | Boolean state-space size |
| `N` | `4` | Number of internal circulation nodes `A1, ..., AN` |
| `beta_Int` | `1 + 0.2 * i` | Internal coupling strength scanned over cases |
| `beta_Ext` | `4` in the main scan | External coupling strength |
| `Simulation_Time_Limit` | `40` | Number of simulated time steps |
| `Start_of_Interaction` | `25` | Time step at which `Ext -> p` becomes active |
| `Size_of_Ensemble` | `10000` | Number of ensemble samples used for estimation |
| `Estimator` | `Simple_Binning` | Histogram/counting estimator for Boolean data |

## Estimated nodes and links

The script records information variables for the selected node and links:

```python
Selected_Nodes = ["p"]
Selected_Links = [("A4", "p"), ("Ext", "p"), ("p", "A1")]
```

For `N != 4`, the first selected link is automatically `("AN", "p")` in the class initialization.
## How to run

From the repository root, run:

```bash
python -m on_Model.015_Boolean_Probability_Update.main
```

or equivalently:

```bash
python on_Model/015_Boolean_Probability_Update/main.py
```

The script runs 10 trials and 10 parameter cases. In case `i`, it sets

```python
beta_Int = 1 + 0.2 * i
beta_Ext = 4
```

After the simulations, it calls `Plot_Data()` to plot the relationship between the pre-interaction internal transfer entropy and the post-interaction external transfer entropy.

## Outputs

Simulation outputs are written under

```text
on_Model/015_Boolean_Probability_Update/Temporal_Results/
```

with the intended structure

```text
Temporal_Results/
  Paper_001/
    Case000/
    Case001/
    ...
  Paper_002/
    Case000/
    ...
```

Typical output files include node-level and link-level time series such as

```text
Node_p.txt
Link_A4_p.txt
Link_Ext_p.txt
Link_p_A1.txt
Simulation_Properties.txt
```

The plotted summary compares

```text
Link_A4_p.txt : TE2 at t = 24
Link_Ext_p.txt : TE2 at t = 25
```

which correspond to the internal information flow just before the external interaction and the external information flow just after the interaction begins.

## Notes and cautions

- The directory-creation lines using `os.mkdir(...)` are currently commented out in `main.py`. Create the output folders manually, or uncomment/add directory creation before running the full scan.
- The random seed is initialized using the current time, so repeated runs are not exactly reproducible unless a fixed seed is set.

## Purpose in the repository

This model provides a minimal Boolean example of competition between an internal circulating information flow and an external input flow at a merging node. It is useful for testing how finite update probability and delayed external coupling affect transfer-entropy allocation in a discrete-state information network.
